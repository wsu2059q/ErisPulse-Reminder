import pytest

from Reminder.Core import Main


@pytest.fixture(scope="session", autouse=True)
def _storage_teardown():
    yield
    from ErisPulse import sdk

    try:
        sdk.storage.close()
    except Exception:
        pass


@pytest.fixture
async def rembot(make_testbot):
    from ErisPulse import i18n

    prev_lang = i18n.get_language()
    i18n.set_language("zh-CN")

    async with make_testbot() as bot:
        await bot.load_module(Main)

        from ErisPulse import module as module_mgr

        rem = module_mgr.get("Reminder")

        cfg = rem.cfg
        cfg.max_reminders_per_user = 20
        cfg.max_duration = "30d"
        cfg.reminder_prefix = "提醒："
        cfg.list_max = 10
        cfg.render_card = False
        rem.cfg = cfg

        from Reminder.Models import Reminder

        await Reminder.delete_all()
        rem._scheduler._handles.clear()

        bot.rem = rem
        yield bot

        await Reminder.delete_all()

    i18n.set_language(prev_lang)
