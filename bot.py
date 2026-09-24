import asyncio
import logging
import os

from aiohttp import web
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from env import BOT_TOKEN

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("string-session-bot")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "👋 Bot is working!\n\nUse /generate to start the session generator."
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "/start - Home\n/generate - Generate a session\n/help - Help"
    )


async def health(request):
    return web.Response(text="String Session Bot is running.")


async def main():
    port = int(os.getenv("PORT", "10000"))

    web_app = web.Application()
    web_app.router.add_get("/", health)
    web_app.router.add_get("/health", health)

    runner = web.AppRunner(web_app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", port).start()
    log.info("Health server listening on port %s", port)

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_cmd))

    await application.initialize()
    me = await application.bot.get_me()
    log.info("Bot API connected: @%s (id=%s)", me.username, me.id)

    await application.start()
    await application.updater.start_polling(drop_pending_updates=True)
    log.info("Telegram Bot API polling started successfully.")

    try:
        await asyncio.Event().wait()
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
