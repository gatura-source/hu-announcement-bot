from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler, filters

from . import handler, task
from .config import TELEGRAM_API_KEY, ANNOUNCEMENT_CHECK_INTERVAL, ANNOUNCEMENT_CHECK_FIRST, WEBHOOK_CONNECTED, PORT, \
    WEBHOOK_URL


def main() -> None:
    app: Application = Application.builder().token(TELEGRAM_API_KEY).build()

    app.add_handler(CommandHandler('start', handler.start), group=1)
    app.add_handler(CommandHandler('help', handler.help), group=1)
    app.add_handler(CommandHandler('reset', handler.reset_subscriptions), group=1)
    app.add_handler(CommandHandler('settings', handler.settings), group=1)
    app.add_handler(CommandHandler('donate', handler.donate), group=1)
    app.add_handler(CommandHandler('answer', handler.answer), group=1)
    app.add_handler(CallbackQueryHandler(handler.settings_buttons), group=1)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('feedback', handler.feedback)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.feedback_done)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, handler.cancel)],
        allow_reentry=True
    ), group=2)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('admin_announcement', handler.admin_announcement)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.admin_announcement_choose_department)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.admin_announcement_done)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, handler.cancel)],
        allow_reentry=True
    ), group=3)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('add', handler.add)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.add_subscription)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, handler.cancel)],
        allow_reentry=True
    ), group=4)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('remove', handler.remove)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.remove_subscription)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, handler.cancel)],
        allow_reentry=True
    ), group=5)

    app.add_error_handler(handler.err_handler)
    app.job_queue.run_repeating(task.check_announcements, interval=ANNOUNCEMENT_CHECK_INTERVAL,
                                first=ANNOUNCEMENT_CHECK_FIRST)

    if WEBHOOK_CONNECTED:
        app.run_webhook(listen="0.0.0.0",
                        port=int(PORT),
                        url_path=TELEGRAM_API_KEY,
                        webhook_url=WEBHOOK_URL)
    else:
        app.run_polling()


if __name__ == "__main__":
    main()
