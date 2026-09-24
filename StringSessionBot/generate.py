import re
from pyrogram import filters
from pyrogram.errors import PhoneCodeInvalid, PhoneCodeExpired
from .basic import cancel
from .session import flows, begin, code, password, export, clear

async def safe_delete(message):
    try:
        await message.delete()
    except Exception:
        pass

def register_generator(app, allowed):
    @app.on_message(filters.command("generate"))
    async def generate(_, message):
        if not await allowed(message):
            return
        flows[message.from_user.id] = "phone"
        await message.reply_text(
            "📱 Send phone number in international format, e.g. +919876543210",
            reply_markup=cancel()
        )

    @app.on_message(filters.private & filters.text)
    async def wizard(_, message):
        uid = message.from_user.id
        state = flows.get(uid)
        if not state or message.text.startswith("/"):
            return
        text = message.text.strip()
        try:
            if state == "phone":
                if not re.fullmatch(r"\+\d{7,15}", text):
                    await message.reply_text("❌ Invalid phone format.")
                    return
                await safe_delete(message)
                await begin(uid, text)
                flows[uid] = "code"
                await message.reply_text(
                    "📨 Telegram sent an OTP. Send it here.",
                    reply_markup=cancel()
                )
            elif state == "code":
                await safe_delete(message)
                needs = await code(uid, text.replace(" ", ""))
                if needs:
                    flows[uid] = "password"
                    await message.reply_text(
                        "🔐 Send your 2FA password.",
                        reply_markup=cancel()
                    )
                else:
                    session = await export(uid)
                    await clear(uid)
                    await message.reply_text(
                        "✅ Session generated. Keep it private.\n\n"
                        f"<code>{session}</code>"
                    )
            elif state == "password":
                await safe_delete(message)
                await password(uid, text)
                session = await export(uid)
                await clear(uid)
                await message.reply_text(
                    "✅ Session generated. Keep it private.\n\n"
                    f"<code>{session}</code>"
                )
        except (PhoneCodeInvalid, PhoneCodeExpired):
            await clear(uid)
            await message.reply_text("❌ OTP invalid or expired. Start again.")
        except Exception:
            await clear(uid)
            await message.reply_text("❌ Login failed. Please try again.")

async def start_flow(message):
    flows[message.from_user.id] = "phone"
    await message.edit_text(
        "📱 Send your Telegram phone number.",
        reply_markup=cancel()
    )

async def clear_flow(uid):
    await clear(uid)
