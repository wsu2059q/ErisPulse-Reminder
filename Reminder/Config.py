from dataclasses import dataclass, field

from ErisPulse.Core.Bases import BaseConfig


@dataclass
class ReminderConfig(BaseConfig):

    max_reminders_per_user: int = field(
        default=20,
        metadata={
            "description": {"i18n": "Reminder.max_reminders_per_user", "default": "单个用户同时挂起的提醒上限"},
            "ui": {"widget": "number", "group": "limit", "order": 1},
        },
    )
    max_duration: str = field(
        default="30d",
        metadata={
            "description": {"i18n": "Reminder.max_duration", "default": "单条提醒的最大时长（如 30d、12h）"},
            "ui": {"widget": "text", "group": "limit", "order": 2},
        },
    )
    reminder_prefix: str = field(
        default="提醒：",
        metadata={
            "description": {"i18n": "Reminder.reminder_prefix", "default": "到期消息的文案前缀"},
            "ui": {"widget": "text", "group": "basic", "order": 3},
        },
    )
    list_max: int = field(
        default=10,
        metadata={
            "description": {"i18n": "Reminder.list_max", "default": "列表单次展示的提醒条数"},
            "ui": {"widget": "number", "group": "report", "order": 4},
        },
    )
    render_card: bool = field(
        default=True,
        metadata={
            "description": {"i18n": "Reminder.render_card", "default": "列表用 Takumi 渲染为卡片（不可用时降级文本）"},
            "ui": {"widget": "switch", "group": "render", "order": 5},
        },
    )
    theme: str = field(
        default="auto",
        metadata={
            "description": {"i18n": "Reminder.theme", "default": "卡片配色 (auto=按时间自动切深浅色)"},
            "ui": {
                "widget": "select",
                "options": ["auto", "light", "dark"],
                "group": "render",
                "order": 6,
            },
        },
    )
