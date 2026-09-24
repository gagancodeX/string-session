from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def home_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 Generate Session", callback_data="generate")],
        [InlineKeyboardButton("❓ Help", callback_data="help"), InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ])

def cancel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]
    ])
