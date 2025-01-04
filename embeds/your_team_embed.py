import discord
from utils.config import bot

async def get_your_team_embed(team):
    embed = discord.Embed(
    title=team['name'],
    description=team['description'],
    color=0xff005a
    )
    embed.add_field(
        name="Indicative ELO",
        value=team['elo'],
        inline=True
    )

    member = await bot.fetch_user(team['captain_id'])
    embed.set_author(name=f"Captain {member.display_name}")
    embed.set_footer(text="Powered By Scream")

    return embed