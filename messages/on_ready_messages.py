import discord

from utils.config import CREATE_A_TEAM_CHANNEL_ID, bot
from embeds.create_team_embed import get_create_team_embed
from buttons.team_buttons import TeamButtons

async def send_messages():
    channel = bot.get_channel(CREATE_A_TEAM_CHANNEL_ID)
    embed = get_create_team_embed()
    view = TeamButtons()

    await channel.purge()
    await channel.send(embed=embed, view=view)