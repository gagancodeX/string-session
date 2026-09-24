import asyncio
import logging
import os

from aiohttp import web
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from env import BOT_TOKEN
from StringSessionBot.generator_ptb import register_generator
from StringSessionBot.session import clear

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("string-session-bot")


def home_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 Generate Session", callback_data="generate")],
        [InlineKeyboardButton("❓ Help", callback_data="help")],
    ])


def cancel_keyboard():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.effective_message.reply_text(
        "👋 Welcome! String Session Bot is online.",
        reply_markup=home_keyboard(),
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "/start - Home\n"
        "/generate - Generate a session\n"
        "/help - Help\n\n"
        "Keep your generated session private.",
        reply_markup=home_keyboard(),
    )


async def generate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "phone"
    await update.effective_message.reply_text(
        "📱 Send your Telegram phone number in international format, e.g. +919876543210",
        reply_markup=cancel_keyboard(),
    )


async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "generate":
        context.user_data["state"] = "phone"
        await query.edit_message_text(
            "📱 Send your Telegram phone number in international format, e.g. +919876543210",
            reply_markup=cancel_keyboard(),
        )
    elif query.data == "help":
        await query.edit_message_text(
            "Use /generate to begin. Never share your session string.",
            reply_markup=home_keyboard(),
        )
    elif query.data == "cancel":
        await clear(query.from_user.id)
        context.user_data.clear()
        await query.edit_message_text(
            "❌ Cancelled.",
            reply_markup=home_keyboard(),
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
    application.add_handler(CommandHandler("generate", generate_cmd))
    application.add_handler(CallbackQueryHandler(callbacks))
    register_generator(application)

    await application.initialize()

    me = await application.bot.get_me()
    log.info("Bot API connected: @%s (id=%s)", me.username, me.id)

    await application.start()
    await application.updater.start_polling(
        drop_pending_updates=True,
        bootstrap_retries=5,
    )
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
