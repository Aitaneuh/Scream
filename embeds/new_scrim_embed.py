import discord
from utils.config import *

def get_new_scrim_embed(team_host, team_request):
    guild = bot.get_guild(GUILD_ID)

    team_host_channel_link = f"https://discord.com/channels/{GUILD_ID}/{team_host['channel_id']}"
    team_request_channel_link = f"https://discord.com/channels/{GUILD_ID}/{team_request['channel_id']}"

    team_host_role = guild.get_role(team_host['role_id'])
    team_request_role = guild.get_role(team_request['role_id'])


    embed = discord.Embed(
    title="NEW SCRIM",
    description=f"{team_host_role.mention} vs {team_request_role.mention}",
    color=0x8d00ff
    )
    embed.add_field(
        name=f"{team_host['name']} Presention",
        value=f"[Click here]({team_host_channel_link})",
        inline=True
    )
    embed.add_field(
        name=f"{team_request['name']} Presention",
        value=f"[Click here]({team_request_channel_link})",
        inline=True
    )

    embed.set_footer(text="Powered By Scream")

    return embed