from discord.ext import commands
import discord
from utils.config import MEMBER_ROLE_ID

async def on_new_member(bot: commands.Bot, member: discord.Member):
    guild = member.guild

    role = discord.utils.get(guild.roles, id=MEMBER_ROLE_ID)

    if role is not None and role not in member.roles:
        await member.add_roles(role)
