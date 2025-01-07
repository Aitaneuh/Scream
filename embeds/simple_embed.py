import discord

def get_simple_embed(content):
    embed = discord.Embed(color=0xffffff, description=content)
    embed.set_footer(text="Powered By Scream")
    embed.timestamp = discord.utils.utcnow()

    return embed