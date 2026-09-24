import asyncio
import logging
import os

# Pyrogram 2.0.106 expects a current asyncio event loop during import.
# Create one explicitly for modern Python versions.
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from aiohttp import web
from pyrogram import Client, filters

from env import API_ID, API_HASH, BOT_TOKEN, MUST_JOIN
from StringSessionBot.basic import home, join_button
from StringSessionBot.bot_users import touch_user
from StringSessionBot.callbacks import register_callbacks
from StringSessionBot.generate import register_generator
from StringSessionBot.must_join import is_joined

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = Client(
    "string-session-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

async def allowed(message):
    if not MUST_JOIN:
        return True
    if await is_joined(app, message.from_user.id, MUST_JOIN):
        return True
    await message.reply_text(
        "🔒 Join the required channel first.",
        reply_markup=join_button(MUST_JOIN)
    )
    return False

@app.on_message(filters.command("start"))
async def start(_, message):
    await touch_user(message.from_user)
    if not await allowed(message):
        return
    await message.reply_text(
        "👋 Welcome! This bot generates a Telegram String Session for your own account.",
        reply_markup=home()
    )

@app.on_message(filters.command("help"))
async def help_cmd(_, message):
    await message.reply_text(
        "/start - Home\n/generate - Generate a session\n/help - Help\n\n"
        "Keep generated session credentials private."
    )

register_callbacks(app, allowed)
register_generator(app, allowed)

async def health(request):
    return web.Response(text="String Session Bot is running.")

async def run_web_server():
    port = int(os.getenv("PORT", "10000"))
    server = web.Application()
    server.router.add_get("/", health)
    server.router.add_get("/health", health)

    runner = web.AppRunner(server)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    log.info("Health server listening on port %s", port)
    return runner

async def main():
    runner = await run_web_server()
    await app.start()
    log.info("Telegram bot started")
    try:
        await asyncio.Event().wait()
    finally:
        await app.stop()
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
