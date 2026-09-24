from .basic import home
from .generate import start_flow, clear_flow
from env import MUST_JOIN
from .must_join import is_joined

def register_callbacks(app, allowed):
    @app.on_callback_query()
    async def callbacks(_, query):
        uid = query.from_user.id
        if query.data == "generate":
            if MUST_JOIN and not await is_joined(app, uid, MUST_JOIN):
                await query.answer("Please join the required channel first.", show_alert=True)
                return
            await start_flow(query.message)
        elif query.data == "check_join":
            if not MUST_JOIN or await is_joined(app, uid, MUST_JOIN):
                await query.message.edit_text(
                    "✅ Verified. Use /generate to continue.",
                    reply_markup=home()
                )
            else:
                await query.answer("Please join first.", show_alert=True)
                return
        elif query.data == "help":
            await query.message.edit_text(
                "Use /generate to begin. Never share your session string."
            )
        elif query.data == "about":
            await query.message.edit_text(
                "⚡ String Session Bot\nIn-memory login; sessions are not stored."
            )
        elif query.data == "cancel":
            await clear_flow(uid)
            await query.message.edit_text("❌ Cancelled.", reply_markup=home())
        await query.answer()
