import discord
from discord.ext import commands
from utils.config import *
from events.on_ready import on_lunch
from events.on_member_join import on_new_member

@bot.event
async def on_ready():
    await on_lunch(bot)

@bot.event
async def on_member_join(member):
    await on_new_member(bot, member)

@bot.command(name="clear")
async def clear(ctx):
    if not ctx.author.guild_permissions.administrator:
        message = discord.Embed(
            title="Access Denied",
            description="You are not an administrator, only administrators can use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=message)
        return
    else:
        await ctx.channel.purge()

bot.run(TOKEN)