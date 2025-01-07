import discord
from utils.config import *

def get_scrim_request_embed(oppenent_team, roster, scrim_message):
    channel_link = f"https://discord.com/channels/{GUILD_ID}/{oppenent_team['channel_id']}"
    embed = discord.Embed(
    title="SCRIM REQUEST",
    description=f"from [{oppenent_team['name']}]({channel_link})",
    color=0x8d00ff
    )
    embed.add_field(
        name="Indicative ELO",
        value=oppenent_team['elo'],
        inline=False
    )
    embed.add_field(
        name="Full Roster",
        value=roster,
        inline=False
    )
    embed.add_field(
        name="Scrim",
        value=scrim_message,
        inline=False
    )

    embed.set_footer(text="Powered By Scream")

    return embed