from dataclasses import dataclass
from typing import Optional
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PasswordHashInvalid
from env import API_ID, API_HASH

@dataclass
class Flow:
    client: Optional[Client] = None
    phone: Optional[str] = None
    phone_code_hash: Optional[str] = None

flows = {}
_sessions = {}

async def begin(uid, phone):
    await clear(uid)
    client = Client(
        f"generator_{uid}",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True
    )
    await client.connect()
    sent = await client.send_code(phone)
    _sessions[uid] = Flow(client, phone, sent.phone_code_hash)

async def code(uid, value):
    flow = _sessions[uid]
    try:
        await flow.client.sign_in(flow.phone, flow.phone_code_hash, value)
        return False
    except SessionPasswordNeeded:
        return True

async def password(uid, value):
    flow = _sessions[uid]
    try:
        await flow.client.check_password(value)
    except PasswordHashInvalid:
        raise ValueError("Invalid 2FA password.")

async def export(uid):
    return await _sessions[uid].client.export_session_string()

async def clear(uid):
    flow = _sessions.pop(uid, None)
    flows.pop(uid, None)
    if flow and flow.client:
        try:
            await flow.client.disconnect()
        except Exception:
            pass
