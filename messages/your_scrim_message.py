import discord
from utils.config import *
from utils.database import *

async def get_your_scrim_message(scrim):
    team = await get_team_by_team_id(scrim['team_id'])

    channel_link = f"https://discord.com/channels/{GUILD_ID}/{team['channel_id']}"

    message = f"🗓️ {scrim['date']}\n⏰ {scrim['time']}\n⚔️ {scrim['best_of']}\n⚙️ {scrim['game_mode']}\n✅ {scrim['elo']}\n✉️ Click the button\n\n🔎 Opponent : [{team['name']}]({channel_link})"

    return message