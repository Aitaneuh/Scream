import discord
import random
import asyncio
from discord.ext import commands
from discord.ui import View, Button
from discord.utils import *
import os
from dotenv import load_dotenv

from utils.config import *
from utils.database import get_db_connection
from events.on_ready import on_lunch
from events.on_member_join import on_new_member


@bot.event
async def on_ready():
    await on_lunch(bot)

@bot.event
async def on_member_join(member):
    await on_new_member(bot, member)

bot.run(TOKEN)
