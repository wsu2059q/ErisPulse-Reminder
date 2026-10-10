<div align="center">

<img src=".github/assets/ErisPulseLogo.png" width="180" alt="ErisPulse Reminder" />

# ErisPulse Reminder

**Reminder module — set timed reminders in chat, auto-restored after restart.**

A lightweight reminder module built on ErisPulse 2.10 owned scheduling (spawn_later) and the built-in ORM, with declarative duration args and restart recovery.

<p>
  <a href="https://pypi.org/project/ErisPulse-Reminder/"><img src="https://img.shields.io/pypi/v/ErisPulse-Reminder?style=for-the-badge&logo=pypi&logoColor=white" alt="PyPI"></a>
  <a href="https://pypi.org/project/ErisPulse-Reminder/"><img src="https://img.shields.io/badge/Python-3.10+-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/ErisPulse/ErisPulse-Reminder"><img src="https://img.shields.io/github/stars/ErisPulse/ErisPulse-Reminder?style=for-the-badge&logo=github&color=brightgreen" alt="Stars"></a>
  <a href="https://pepy.tech/project/ErisPulse-Reminder"><img src="https://img.shields.io/pepy/dt/ErisPulse-Reminder?style=for-the-badge&color=blue" alt="Downloads"></a>
  <a href="https://github.com/ErisPulse/ErisPulse"><img src="https://img.shields.io/badge/Powered_by-ErisPulse-FF6B9D?style=for-the-badge&logo=bookstack&logoColor=white" alt="ErisPulse"></a>
</p>

<p>
  <a href="./README.md">简体中文</a> | <a href="./README.en.md">English</a>
</p>

</div>

---

## Introduction

Reminder is a lightweight reminder module for the [ErisPulse](https://github.com/ErisPulse/ErisPulse/) framework:

- `/提醒 30m drink water`: declarative duration args (`90s` / `1h30m` / `1d` auto-converted to seconds)
- Fires via the adapter to the original session (private or group)
- Records persist with the built-in ORM and **restore after restart**: pending ones rescheduled, overdue ones fired immediately
- Scheduling tasks are owned (`spawn_later` owner), auto-cancelled on module unload
- Per-user pending limit, per-reminder duration limit, text length constraint
- Lists render as Takumi cards, falling back to text

Requires ErisPulse >= 2.10.0.

---

## Installation

```bash
epsdk install ErisPulse-Reminder
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/提醒 <duration> <text>` | Set a reminder, e.g. `/提醒 30m drink water` |
| `/提醒 列表` | List your pending reminders |
| `/提醒 取消 <id>` | Cancel a reminder |

Duration syntax: `90s`, `30m`, `2h`, `1d`, combinable like `1h30m`.

---

## Configuration

```toml
[Reminder]
max_reminders_per_user = 20     # max pending reminders per user
max_duration = "30d"            # max duration of one reminder
reminder_prefix = "提醒："       # due message prefix
list_max = 10                   # max entries per list
render_card = true              # render lists as image cards
theme = "doodle"                  # card style (doodle/editorial)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `max_reminders_per_user` | int | `20` | Per-user pending limit |
| `max_duration` | str | `30d` | Max duration |
| `reminder_prefix` | str | `提醒：` | Due message prefix |
| `list_max` | int | `10` | Max entries per list |
| `render_card` | bool | `true` | Card rendering |
| `theme` | str | `doodle` | Card style (doodle/editorial) |

---

## Notes

1. On delivery failure the reminder is still marked done (no infinite retry); failures are logged
2. Reminders fire into the session where they were set (group messages go back to the group)
3. Records live in the framework storage backend, migrating with your data backups

---

## References

- [ErisPulse](https://github.com/ErisPulse/ErisPulse/)
- [Runtime scheduling docs](https://github.com/ErisPulse/ErisPulse/tree/main/docs/zh-CN/advanced/connections.md)
- [ORM docs](https://github.com/ErisPulse/ErisPulse/tree/main/docs/zh-CN/developer-guide/orm.md)
