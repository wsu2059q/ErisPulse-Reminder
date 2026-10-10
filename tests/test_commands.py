import asyncio
import time

from ErisPulse_Testing import create_command_event

from Reminder.Models import Reminder


async def _wait_for(predicate, timeout=6.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if await predicate():
            return True
        await asyncio.sleep(0.1)
    return False


async def _created_ids():
    rows = await Reminder.where(Reminder.status == "pending").all()
    return sorted(r.id for r in rows)


async def test_remind_usage(rembot):
    await rembot.dispatch(create_command_event("提醒"))
    rembot.assert_reply_contains("用法")


async def test_remind_create(rembot):
    await rembot.dispatch(create_command_event("提醒 10m 喝水"))
    rows = await Reminder.where(Reminder.status == "pending").all()
    assert len(rows) == 1
    rid = rows[0].id
    rembot.assert_reply_contains(f"提醒 #{rid} 已设置")
    assert rows[0].text == "喝水"
    assert rows[0].user_id == "tester"
    assert rows[0].platform == "test"
    assert 500 <= rows[0].due_at - time.time() <= 700
    assert rid in rembot.rem._scheduler._handles


async def test_remind_create_group(rembot):
    await rembot.dispatch(create_command_event("提醒 5m 开会", group_id="g100"))
    rows = await Reminder.where(Reminder.status == "pending").all()
    assert rows[0].target_type == "group"
    assert rows[0].target_id == "g100"


async def test_remind_invalid_duration(rembot):
    await rembot.dispatch(create_command_event("提醒 abc 喝水"))
    assert await Reminder.count() == 0


async def test_remind_duration_too_long(rembot):
    cfg = rembot.rem.cfg
    cfg.max_duration = "1h"
    rembot.rem.cfg = cfg
    await rembot.dispatch(create_command_event("提醒 2d 太久了"))
    rembot.assert_reply_contains("时长超过上限 1h")
    assert await Reminder.count() == 0


async def test_remind_text_too_long(rembot):
    await rembot.dispatch(create_command_event("提醒 10m " + "长" * 501))
    rembot.assert_reply_contains("超过 500 字")
    assert await Reminder.count() == 0


async def test_remind_quota(rembot):
    cfg = rembot.rem.cfg
    cfg.max_reminders_per_user = 2
    rembot.rem.cfg = cfg
    await rembot.dispatch(create_command_event("提醒 10m a"))
    await rembot.dispatch(create_command_event("提醒 10m b"))
    await rembot.dispatch(create_command_event("提醒 10m c"))
    rembot.assert_reply_contains("已达 2 条（上限 2）")
    assert await Reminder.count() == 2


async def test_remind_list_and_cancel(rembot):
    await rembot.dispatch(create_command_event("提醒 1h 第一件事"))
    await rembot.dispatch(create_command_event("提醒 2h 第二件事"))
    ids = await _created_ids()
    assert len(ids) == 2

    await rembot.dispatch(create_command_event("提醒 列表"))
    reply = rembot.last_reply.text
    assert "待触发提醒（2 条）" in reply
    assert f"#{ids[0]}" in reply
    assert "第一件事" in reply

    await rembot.dispatch(create_command_event(f"提醒 取消 {ids[0]}"))
    rembot.assert_reply_contains(f"提醒 #{ids[0]} 已取消")
    row = await Reminder.get(id=ids[0])
    assert row.status == "canceled"
    assert ids[0] not in rembot.rem._scheduler._handles

    await rembot.dispatch(create_command_event("提醒 列表"))
    reply = rembot.last_reply.text
    assert "待触发提醒（1 条）" in reply
    assert "第二件事" in reply


async def test_remind_cancel_not_owned(rembot):
    now = time.time()
    row = await Reminder.create(
        platform="test", target_type="user", target_id="other",
        user_id="someone_else", due_at=now + 600,
        text="别人的", status="pending", created_at=now,
    )
    await rembot.dispatch(create_command_event(f"提醒 取消 {row.id}"))
    rembot.assert_reply_contains("不存在或不属于你")


async def test_remind_list_empty(rembot):
    await rembot.dispatch(create_command_event("提醒 列表"))
    rembot.assert_reply_contains("没有待触发的提醒")


async def test_remind_fires_and_marks_done(rembot):
    await rembot.dispatch(create_command_event("提醒 1s 到点测试"))
    rows = await Reminder.where(Reminder.status == "pending").all()
    rid = rows[0].id
    rembot.assert_reply_contains("已设置")

    async def delivered():
        return any("到点测试" in (r.text or "") for r in rembot.replies)

    assert await _wait_for(delivered), "提醒未在时限内送达"
    row = await Reminder.get(id=rid)
    assert row.status == "done"
    assert rid not in rembot.rem._scheduler._handles
