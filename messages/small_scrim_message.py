async def get_small_scrim_message(scrim):
    message = f"🗓️ {scrim['date']}\n⏰ {scrim['time']}\n⚔️ {scrim['best_of']}\n⚙️ {scrim['game_mode']}\n✅ {scrim['elo']}\n✉️ Clich the button"
    return message