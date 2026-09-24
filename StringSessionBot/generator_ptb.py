import re
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, MessageHandler, filters
from pyrogram.errors import PhoneCodeExpired, PhoneCodeInvalid

from StringSessionBot.session import begin, clear, code as verify_code, export, password

log = logging.getLogger("string-session-generator")


def cancel_keyboard():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]
    )


async def wizard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = update.effective_user
    if not message or not user or not message.text:
        return

    state = context.user_data.get("state")
    if not state or message.text.startswith("/"):
        return

    value = message.text.strip()
    uid = user.id

    try:
        if state == "phone":
            if not re.fullmatch(r"\+\d{7,15}", value):
                await message.reply_text(
                    "❌ Invalid phone format. Example: +919876543210",
                    reply_markup=cancel_keyboard(),
                )
                return
            await message.delete()
            await begin(uid, value)
            context.user_data["state"] = "code"
            await message.reply_text(
                "📨 Telegram sent an OTP. Send it here.",
                reply_markup=cancel_keyboard(),
            )
            return

        if state == "code":
            await message.delete()
            needs_password = await verify_code(uid, value.replace(" ", ""))
            if needs_password:
                context.user_data["state"] = "password"
                await message.reply_text(
                    "🔐 Send your 2FA password.",
                    reply_markup=cancel_keyboard(),
                )
            else:
                session = await export(uid)
                await clear(uid)
                context.user_data.clear()
                await message.reply_text(
                    "✅ Session generated. Keep it private.\\n\\n" + f"<code>{session}</code>",
                    parse_mode="HTML",
                )
            return

        if state == "password":
            await message.delete()
            await password(uid, value)
            session = await export(uid)
            await clear(uid)
            context.user_data.clear()
            await message.reply_text(
                "✅ Session generated. Keep it private.\\n\\n" + f"<code>{session}</code>",
                parse_mode="HTML",
            )

    except (PhoneCodeInvalid, PhoneCodeExpired):
        await clear(uid)
        context.user_data.clear()
        await message.reply_text("❌ OTP invalid or expired. Start again.")
    except Exception:
        log.exception("Generator flow failed for user_id=%s", uid)
        await clear(uid)
        context.user_data.clear()
        await message.reply_text("❌ Login failed. Please try again.")


def register_generator(application):
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, wizard)
    )
