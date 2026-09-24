import os
from dotenv import load_dotenv

load_dotenv()

def required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

BOT_TOKEN = required("BOT_TOKEN")
API_ID = int(required("API_ID"))
API_HASH = required("API_HASH")
