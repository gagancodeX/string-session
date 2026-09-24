async def is_joined(app, user_id, channel):
    try:
        member = await app.get_chat_member(channel, user_id)
        return member.status not in ("left", "kicked")
    except Exception:
        return False
