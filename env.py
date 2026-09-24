import os
from dotenv import load_dotenv

load_dotenv()

def required(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

API_ID = int(required("API_ID"))
API_HASH = required("API_HASH")
BOT_TOKEN = required("BOT_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI", "").strip()
MUST_JOIN = os.getenv("MUST_JOIN", "").strip()
