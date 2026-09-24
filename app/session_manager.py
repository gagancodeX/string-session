from dataclasses import dataclass
from typing import Optional
from pyrogram import Client
from pyrogram.errors import PasswordHashInvalid, SessionPasswordNeeded
from .config import API_HASH, API_ID

@dataclass
class SessionFlow:
    client: Optional[Client] = None
    phone: Optional[str] = None
    phone_code_hash: Optional[str] = None

_flows: dict[int, SessionFlow] = {}

async def cleanup(user_id: int) -> None:
    flow = _flows.pop(user_id, None)
    if flow and flow.client:
        try:
            await flow.client.disconnect()
        except Exception:
            pass

async def start_login(user_id: int, phone: str) -> None:
    await cleanup(user_id)
    client = Client(
        name=f"generator_{user_id}",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True,
    )
    await client.connect()
    sent = await client.send_code(phone)
    _flows[user_id] = SessionFlow(client=client, phone=phone, phone_code_hash=sent.phone_code_hash)

async def submit_code(user_id: int, code: str) -> bool:
    flow = _flows[user_id]
    if not flow.client or not flow.phone or not flow.phone_code_hash:
        raise RuntimeError("Session flow expired.")
    try:
        await flow.client.sign_in(flow.phone, flow.phone_code_hash, code)
        return False
    except SessionPasswordNeeded:
        return True

async def submit_password(user_id: int, password: str) -> None:
    flow = _flows[user_id]
    if not flow.client:
        raise RuntimeError("Session flow expired.")
    try:
        await flow.client.check_password(password)
    except PasswordHashInvalid:
        raise ValueError("Invalid 2FA password.")

async def export_session(user_id: int) -> str:
    flow = _flows[user_id]
    if not flow.client:
        raise RuntimeError("Session flow expired.")
    return await flow.client.export_session_string()
