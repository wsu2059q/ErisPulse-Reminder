from ErisPulse.Core.Bases import BaseI18n, I18nKey


class ReminderI18n(BaseI18n):

    max_reminders_per_user: I18nKey = I18nKey(
        default="Max pending reminders per user",
        zh_CN="单个用户同时挂起的提醒上限",
        zh_TW="單個用戶同時掛起的提醒上限",
        en="Max pending reminders per user",
        ja="ユーザーごとの保留リマインダー上限",
        ru="Максимум отложенных напоминаний на пользователя",
    )
    max_duration: I18nKey = I18nKey(
        default="Max duration of one reminder (e.g. 30d, 12h)",
        zh_CN="单条提醒的最大时长（如 30d、12h）",
        zh_TW="單條提醒的最大時長（如 30d、12h）",
        en="Max duration of one reminder (e.g. 30d, 12h)",
        ja="1件のリマインダーの最大期間（例: 30d、12h）",
        ru="Максимальная длительность одного напоминания (напр. 30d, 12h)",
    )
    reminder_prefix: I18nKey = I18nKey(
        default="Text prefix of the due message",
        zh_CN="到期消息的文案前缀",
        zh_TW="到期訊息的文案前綴",
        en="Text prefix of the due message",
        ja="期日メッセージの接頭辞",
        ru="Префикс текста напоминания",
    )
    list_max: I18nKey = I18nKey(
        default="Max reminders shown in one list",
        zh_CN="列表单次展示的提醒条数",
        zh_TW="列表單次展示的提醒條數",
        en="Max reminders shown in one list",
        ja="リスト1回の最大表示件数",
        ru="Максимум напоминаний в одном списке",
    )
    render_card: I18nKey = I18nKey(
        default="Render lists as image cards via Takumi (fallback to text)",
        zh_CN="列表用 Takumi 渲染为卡片（不可用时降级文本）",
        zh_TW="列表用 Takumi 渲染為卡片（不可用時降級文本）",
        en="Render lists as image cards via Takumi (fallback to text)",
        ja="リストを Takumi でカード画像化（不可時はテキスト）",
        ru="Рендер списков в карточки через Takumi (иначе текст)",
    )
    theme: I18nKey = I18nKey(
        default="Card color theme (auto = light/dark by time)",
        zh_CN="卡片配色 (auto=按时间自动切深浅色)",
        zh_TW="卡片配色 (auto=按時間自動切深淺色)",
        en="Card color theme (auto = light/dark by time)",
        ja="カード配色（auto=時間で自動切替）",
        ru="Тема карточек (auto = светлая/тёмная по времени)",
    )
    module_loaded: I18nKey = I18nKey(
        default="Reminder loaded: {event}",
        zh_CN="提醒模块已加载: {event}",
        zh_TW="提醒模組已載入: {event}",
        en="Reminder loaded: {event}",
        ja="Reminder を読み込みました: {event}",
        ru="Reminder загружен: {event}",
    )
    module_unloaded: I18nKey = I18nKey(
        default="Reminder unloaded: {event}",
        zh_CN="提醒模块已卸载: {event}",
        zh_TW="提醒模組已卸載: {event}",
        en="Reminder unloaded: {event}",
        ja="Reminder を解除しました: {event}",
        ru="Reminder выгружен: {event}",
    )
    created: I18nKey = I18nKey(
        default="Reminder #{id} set, due at {time}",
        zh_CN="提醒 #{id} 已设置，将在 {time} 触发",
        zh_TW="提醒 #{id} 已設定，將在 {time} 觸發",
        en="Reminder #{id} set, due at {time}",
        ja="リマインダー #{id} を設定しました。{time} に通知",
        ru="Напоминание #{id} установлено, сработает в {time}",
    )
    list_empty: I18nKey = I18nKey(
        default="No pending reminders",
        zh_CN="没有待触发的提醒",
        zh_TW="沒有待觸發的提醒",
        en="No pending reminders",
        ja="保留中のリマインダーはありません",
        ru="Нет отложенных напоминаний",
    )
    list_header: I18nKey = I18nKey(
        default="Pending reminders ({count}):",
        zh_CN="待触发提醒（{count} 条）：",
        zh_TW="待觸發提醒（{count} 條）：",
        en="Pending reminders ({count}):",
        ja="保留中のリマインダー（{count} 件）：",
        ru="Отложенные напоминания ({count}):",
    )
    canceled: I18nKey = I18nKey(
        default="Reminder #{id} canceled",
        zh_CN="提醒 #{id} 已取消",
        zh_TW="提醒 #{id} 已取消",
        en="Reminder #{id} canceled",
        ja="リマインダー #{id} をキャンセルしました",
        ru="Напоминание #{id} отменено",
    )
    cancel_not_found: I18nKey = I18nKey(
        default="Reminder #{id} not found or not yours",
        zh_CN="提醒 #{id} 不存在或不属于你",
        zh_TW="提醒 #{id} 不存在或不屬於你",
        en="Reminder #{id} not found or not yours",
        ja="リマインダー #{id} が見つからないか所有者ではありません",
        ru="Напоминание #{id} не найдено или не ваше",
    )
    quota_exceeded: I18nKey = I18nKey(
        default="You have {count} pending reminders (max {limit})",
        zh_CN="你的待触发提醒已达 {count} 条（上限 {limit}）",
        zh_TW="你的待觸發提醒已達 {count} 條（上限 {limit}）",
        en="You have {count} pending reminders (max {limit})",
        ja="保留中のリマインダーが {count} 件に達しました（上限 {limit}）",
        ru="У вас {count} отложенных напоминаний (максимум {limit})",
    )
    duration_too_long: I18nKey = I18nKey(
        default="Duration exceeds the limit {max}",
        zh_CN="时长超过上限 {max}",
        zh_TW="時長超過上限 {max}",
        en="Duration exceeds the limit {max}",
        ja="期間が上限 {max} を超えています",
        ru="Длительность превышает лимит {max}",
    )
    text_too_long: I18nKey = I18nKey(
        default="Reminder text exceeds {max} characters",
        zh_CN="提醒内容超过 {max} 字",
        zh_TW="提醒內容超過 {max} 字",
        en="Reminder text exceeds {max} characters",
        ja="リマインダー本文が {max} 文字を超えています",
        ru="Текст напоминания превышает {max} символов",
    )
    restored: I18nKey = I18nKey(
        default="Restored {count} pending reminder(s) after restart",
        zh_CN="重启后恢复了 {count} 条待触发提醒",
        zh_TW="重啟後恢復了 {count} 條待觸發提醒",
        en="Restored {count} pending reminder(s) after restart",
        ja="再起動後に {count} 件のリマインダーを復元しました",
        ru="После перезапуска восстановлено напоминаний: {count}",
    )
