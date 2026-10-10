import asyncio
import time

from ErisPulse_Testing import create_command_event

from Reminder.Models import Reminder


async def _reload_module():
    from ErisPulse import module as module_mgr

    await module_mgr.unload("Reminder")
    ok = await module_mgr.load("Reminder")
    return module_mgr.get("Reminder")


async def test_restore_schedules_pending(rembot):
    now = time.time()
    row = await Reminder.create(
        platform="test", target_type="user", target_id="tester",
        user_id="tester", due_at=now + 3600,
        text="一小时后的", status="pending", created_at=now,
    )

    rem = await _reload_module()
    assert rem is not None
    await asyncio.sleep(0.2)
    assert row.id in rem._scheduler._handles


async def test_restore_overdue_fires(rembot):
    now = time.time()
    row = await Reminder.create(
        platform="test", target_type="user", target_id="tester",
        user_id="tester", due_at=now - 60,
        text="错过的提醒", status="pending", created_at=now - 120,
    )

    rem = await _reload_module()

    async def delivered():
        return any("错过的提醒" in (r.text or "") for r in rembot.replies)

    deadline = time.time() + 6
    ok = False
    while time.time() < deadline:
        if await delivered():
            ok = True
            break
        await asyncio.sleep(0.1)
    assert ok, "过期提醒未补发"
    fresh = await Reminder.get(id=row.id)
    assert fresh.status == "done"


async def test_unload_cancels_handles(rembot):
    await rembot.dispatch(create_command_event("提醒 30m 未到期的"))
    rows = await Reminder.where(Reminder.status == "pending").all()
    assert len(rembot.rem._scheduler._handles) == 1

    from ErisPulse import module as module_mgr

    await module_mgr.unload("Reminder")
    assert rembot.rem._scheduler._handles == {}
    await module_mgr.load("Reminder")
