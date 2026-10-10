import time

from ErisPulse import spawn_later

from .Models import Reminder

MIN_DELAY = 1.0


class ReminderScheduler:

    def __init__(self, sdk, logger):
        self.sdk = sdk
        self.logger = logger
        self._handles: dict[int, object] = {}
        self._firing: set[int] = set()

    def schedule(self, reminder_id: int, delay: float) -> None:
        self.cancel(reminder_id)
        if delay < MIN_DELAY:
            delay = MIN_DELAY
        handle = spawn_later(delay, self.fire, reminder_id, owner="Reminder")
        self._handles[reminder_id] = handle

    def cancel(self, reminder_id: int) -> None:
        handle = self._handles.pop(reminder_id, None)
        if handle is not None:
            try:
                handle.cancel()
            except Exception:
                pass

    async def fire(self, reminder_id: int) -> None:
        self._handles.pop(reminder_id, None)
        try:
            row = await Reminder.get(id=reminder_id)
        except Exception as e:
            self.logger.warning(f"读取提醒 #{reminder_id} 失败: {e}")
            return
        if row is None or row.status != "pending":
            return
        if row.due_at > time.time() + 1.0:
            self.schedule(reminder_id, row.due_at - time.time())
            return

        prefix = "提醒："
        try:
            from ErisPulse import module as module_mgr

            inst = module_mgr.get("Reminder")
            if inst is not None:
                prefix = inst.cfg.reminder_prefix or prefix
        except Exception:
            pass

        sent = False
        try:
            adapter = self.sdk.adapter.get(row.platform)
            await adapter.Send.To(row.target_type, row.target_id).Text(prefix + row.text)
            sent = True
        except Exception as e:
            self.logger.warning(f"提醒 #{reminder_id} 发送失败: {e}")

        row.status = "done"
        try:
            await row.save()
        except Exception as e:
            self.logger.warning(f"提醒 #{reminder_id} 状态更新失败: {e}")
        if sent:
            self.logger.info(f"提醒 #{reminder_id} 已送达 {row.platform}/{row.target_type}/{row.target_id}")

    async def restore(self) -> int:
        now = time.time()
        rows = await Reminder.where(Reminder.status == "pending").all()
        for row in rows:
            delay = row.due_at - now
            if delay < MIN_DELAY:
                self.schedule(row.id, MIN_DELAY)
            else:
                self.schedule(row.id, delay)
        return len(rows)

    async def shutdown(self) -> None:
        for reminder_id in list(self._handles):
            self.cancel(reminder_id)
