# String Session Bot

A clean Telegram String Session generator built with Pyrogram.

Security: A Telegram String Session is a sensitive account credential. This bot generates a session for the user and returns it without intentionally saving generated sessions to a database or file.

## Features
- /start welcome menu
- /generate session wizard
- /help and /about
- Phone + OTP authentication
- Optional Telegram 2FA password
- Cancel button
- Sensitive input messages are deleted when possible
- No session persistence
- Render worker compatible

## Setup
1. Create a bot with BotFather and get BOT_TOKEN.
2. Get a Telegram API_ID and API_HASH from my.telegram.org.
3. Copy .env.example to .env.
4. Fill the environment variables.
5. Install: pip install -r requirements.txt
6. Run: python -m app.bot

## Environment
BOT_TOKEN=your_bot_token
API_ID=123456
API_HASH=your_api_hash

## Render
Use a Background Worker.
Build command: pip install -r requirements.txt
Start command: python -m app.bot

Add BOT_TOKEN, API_ID, and API_HASH as Render environment variables.

Important: Never publish your .env, bot token, API hash, or generated String Sessions. Anyone who obtains a valid String Session may be able to access the associated Telegram account.

This project is independently implemented and is not a copy of any reference repository.
