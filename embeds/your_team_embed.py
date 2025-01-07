import discord
from utils.config import bot

async def get_your_team_embed(team):
    captain = await bot.fetch_user(team['captain_id'])
    header = "---------------{description}---------------"
    embed = discord.Embed(
    title=team['name'],
    description=f"{header}\n{team['description']}\n-------------------------------------------\n\nCaptain : {captain.mention}",
    color=0x0013ff
    )
    embed.add_field(
        name="Indicative ELO",
        value=team['elo'],
        inline=False
    )

    embed.set_footer(text="Powered By Scream")

    return embed