import discord
from utils.config import *

def get_scrim_decline_embed(host_team, scrim_message):
    channel_link = f"https://discord.com/channels/{GUILD_ID}/{host_team['channel_id']}"
    embed = discord.Embed(
    title="SCRIM REQUEST DECLINED",
    description=f"declined by [{host_team['name']}]({channel_link})",
    color=0x8d00ff
    )
    embed.add_field(
        name="Scrim",
        value=scrim_message,
        inline=False
    )

    embed.set_footer(text="Powered By Scream")

    return embed