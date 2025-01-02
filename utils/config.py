import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

activity = discord.Game(name="Scream")
bot = commands.Bot(
    command_prefix="!", 
    intents=discord.Intents.all(), 
    activity=activity, 
    status=discord.Status.online
)

MEMBER_ROLE_ID = 1324421516032479253