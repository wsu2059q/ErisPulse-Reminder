import time
from datetime import datetime

from ErisPulse import i18n, sdk
from ErisPulse.Core.Bases import BaseModule, ModuleMeta
from ErisPulse.Core.Event import command
from ErisPulse.loaders import ModuleLoadStrategy

from .Config import ReminderConfig
from .I18n import ReminderI18n
from .Models import Reminder
from .Scheduler import ReminderScheduler
from .Visualizer import CardVisualizer

TEXT_MAX = 500


def _fmt_due(due_at: float) -> str:
    return datetime.fromtimestamp(due_at).strftime("%m-%d %H:%M:%S")


def _fmt_in(seconds: float) -> str:
    seconds = max(0, int(seconds))
    if seconds < 60:
        return f"{seconds}秒"
    if seconds < 3600:
        return f"{seconds // 60}分{seconds % 60}秒"
    if seconds < 86400:
        return f"{seconds // 3600}时{(seconds % 3600) // 60}分"
    return f"{seconds // 86400}天{(seconds % 86400) // 3600}时"


class Main(BaseModule):

    ConfigClass = ReminderConfig
    I18nClass = ReminderI18n

    def __init__(self):
        self.sdk = sdk
        self.logger = sdk.logger.get_child("Reminder")
        self._scheduler = ReminderScheduler(sdk, self.logger)
        self._viz = CardVisualizer(sdk, self.logger)

    @staticmethod
    def get_load_strategy() -> ModuleLoadStrategy:
        return ModuleLoadStrategy(lazy_load=False, priority=30)

    @staticmethod
    def get_meta() -> ModuleMeta:
        return ModuleMeta(
            name="Reminder",
            description="提醒模块：/提醒 <时长> <内容> 定时提醒，重启自动恢复",
            version="0.1.0",
            author="ErisPulse-devs",
            group="工具",
            tags=["提醒", "定时", "spawn_later", "ORM"],
            min_sdk_version="2.10.0",
        )

    async def on_load(self, event: dict) -> bool:
        await Reminder.create_table()
        count = await self._scheduler.restore()
        if count:
            self.logger.info(i18n.t("Reminder.restored", count=count))

        self._register_commands()
        self.logger.info(i18n.t("Reminder.module_loaded", event=event))
        return True

    async def on_unload(self, event: dict) -> bool:
        await self._scheduler.shutdown()
        self.logger.info(i18n.t("Reminder.module_unloaded", event=event))
        return True

    def _session_target(self, event):
        platform = event.get_platform()
        if event.is_group_message():
            target_type, target_id = "group", event.get_group_id()
        else:
            target_type, target_id = "user", event.get_user_id()
        if not platform or not target_id:
            return None
        return platform, target_type, str(target_id)

    def _max_duration_secs(self) -> float:
        from ErisPulse.Core.Event import command_args

        try:
            return float(command_args.parse_duration(self.cfg.max_duration) or 0)
        except Exception:
            return 0.0

    def _register_commands(self):
        @command("提醒", help="设置提醒: /提醒 <时长> <内容>，如 /提醒 30m 喝水",
                 args="<time:duration> <text:rest>")
        async def remind_handler(event, time: float = 0.0, text: str = ""):
            await self._create_reminder(event, time, text)

        @command("提醒 列表", help="查看我的待触发提醒")
        async def remind_list_handler(event):
            await self._reply_list(event)

        @command("提醒 取消", help="取消提醒: /提醒 取消 <编号>", args="<id:int>")
        async def remind_cancel_handler(event, id: int):
            await self._cancel_reminder(event, id)

    async def _create_reminder(self, event, seconds: float, text: str):
        text = (text or "").strip()
        if seconds <= 0 or not text:
            await event.reply("用法: /提醒 <时长> <内容>（如 /提醒 30m 喝水）")
            return

        max_secs = self._max_duration_secs()
        if max_secs > 0 and seconds > max_secs:
            await event.reply(i18n.t("Reminder.duration_too_long", max=self.cfg.max_duration))
            return
        if len(text) > TEXT_MAX:
            await event.reply(i18n.t("Reminder.text_too_long", max=TEXT_MAX))
            return

        user_id = str(event.get_user_id() or "")
        target = self._session_target(event)
        if target is None:
            await event.reply("无法识别当前会话，设置提醒失败")
            return
        platform, target_type, target_id = target

        used = await Reminder.count(
            (Reminder.user_id == user_id) & (Reminder.status == "pending")
        )
        if used >= self.cfg.max_reminders_per_user:
            await event.reply(i18n.t(
                "Reminder.quota_exceeded", count=used, limit=self.cfg.max_reminders_per_user,
            ))
            return

        try:
            row = await Reminder.create(
                platform=platform,
                target_type=target_type,
                target_id=target_id,
                user_id=user_id,
                due_at=time.time() + seconds,
                text=text,
                status="pending",
                created_at=time.time(),
            )
        except ValueError as e:
            await event.reply(f"设置失败: {e}")
            return

        self._scheduler.schedule(row.id, seconds)
        await event.reply(i18n.t("Reminder.created", id=row.id, time=_fmt_due(row.due_at)))

    async def _pending_rows(self, event):
        user_id = str(event.get_user_id() or "")
        now = time.time()
        rows = await Reminder.where(
            (Reminder.user_id == user_id) & (Reminder.status == "pending")
        ).order_by("due_at").all()
        return now, rows

    async def _reply_list(self, event):
        now, rows = await self._pending_rows(event)
        if not rows:
            await event.reply(i18n.t("Reminder.list_empty"))
            return

        shown = rows[: self.cfg.list_max]
        lines = [i18n.t("Reminder.list_header", count=len(rows))]
        for row in shown:
            lines.append(f"#{row.id} · {_fmt_due(row.due_at)}（{_fmt_in(row.due_at - now)}后）· {row.text[:40]}")
        hidden = len(rows) - len(shown)
        if hidden > 0:
            lines.append(f"…其余 {hidden} 条已省略")
        await self._reply_card(
            event,
            self._list_card_html(event, now, rows),
            "\n".join(lines),
        )

    def _list_card_html(self, event, now: float, rows: list) -> str:
        shown = rows[: self.cfg.list_max]
        if shown:
            body_rows = []
            for row in shown:
                overdue = row.due_at <= now
                chips = self._viz.chips([
                    f"{_fmt_due(row.due_at)}",
                    ("已到期" if overdue else f"{_fmt_in(row.due_at - now)}后"),
                    f"{row.platform}/{row.target_type}",
                ])
                body_rows.append(self._viz.count_row(
                    f"#{row.id}", "", (row.text[:60] + "…") if len(row.text) > 60 else row.text, chips,
                ))
            body = "".join(body_rows)
        else:
            body = "<div class='empty'>没有待触发的提醒</div>"
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            self._viz.head("待触发提醒", f"共 {len(rows)} 条")
            + f"<div class='body'>{body}</div>"
            + self._viz.foot(f"Reminder · {stamp}", f"展示 {len(shown)} / {len(rows)}")
        )

    async def _cancel_reminder(self, event, reminder_id: int):
        user_id = str(event.get_user_id() or "")
        row = await Reminder.get(id=reminder_id)
        if row is None or row.user_id != user_id or row.status != "pending":
            await event.reply(i18n.t("Reminder.cancel_not_found", id=reminder_id))
            return
        row.status = "canceled"
        await row.save()
        self._scheduler.cancel(reminder_id)
        await event.reply(i18n.t("Reminder.canceled", id=reminder_id))

    async def _reply_card(self, event, html, fallback_text: str):
        if self.cfg.render_card:
            png = await self._viz.render(html, theme=self.cfg.theme)
            if png is not None:
                try:
                    await event.reply(png, method="Image")
                    return
                except Exception as e:
                    self.logger.warning(f"图片回复失败，降级文本: {e}")
        await event.reply(fallback_text)
