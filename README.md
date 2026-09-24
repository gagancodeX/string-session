# String Session Bot

An independently implemented Pyrogram Telegram String Session Generator.

## Features
- /start, /generate, /help
- Optional MUST_JOIN
- Optional MongoDB for basic bot-user metadata
- In-memory Telegram login flow
- Generated session strings are not stored in MongoDB
- Render/Heroku-style worker support

## Environment
API_ID=
API_HASH=
BOT_TOKEN=
MONGODB_URI=
MUST_JOIN=

Never commit real secrets or generated session strings.

## Run
pip install -r requirements.txt
python bot.py

For Render use a Background Worker with start command:
python bot.py

Only use the generator with Telegram accounts you own or are authorized to access.
