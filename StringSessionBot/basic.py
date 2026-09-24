from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def home():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 Generate Session", callback_data="generate")],
        [InlineKeyboardButton("❓ Help", callback_data="help"),
         InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ])

def cancel():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]
    ])

def join_button(channel):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{channel.lstrip('@')}")],
        [InlineKeyboardButton("✅ Check Again", callback_data="check_join")]
    ])
