import discord

from utils.config import *
from embeds.create_team_embed import get_create_team_embed
from embeds.team_utils_embed import get_team_utils_embed
from buttons.create_team_buttons import CreateTeamButtons
from buttons.utils_buttons import UtilsButtons

async def send_messages():
    create_a_team_channel = bot.get_channel(CREATE_A_TEAM_CHANNEL_ID)
    create_a_team_embed = get_create_team_embed()
    create_a_team_view = CreateTeamButtons()

    await create_a_team_channel.purge()
    await create_a_team_channel.send(embed=create_a_team_embed, view=create_a_team_view)

    team_utils_channel = bot.get_channel(TEAM_UTILS_CHANNEL_ID)
    team_utils_embed = get_team_utils_embed()
    team_utils_view = UtilsButtons()

    await team_utils_channel.purge()
    await team_utils_channel.send(embed=team_utils_embed, view=team_utils_view)