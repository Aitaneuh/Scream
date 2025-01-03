import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

ACTIVITY_NAME = "scrim cause he wants to be better"

activity = discord.Game(name=ACTIVITY_NAME)
bot = commands.Bot(
    command_prefix="!", 
    intents=discord.Intents.all(), 
    activity=activity, 
    status=discord.Status.online
)

MEMBER_ROLE_ID = 1324421516032479253

TEAM_UTILS_CHANNEL_ID = 1324442708571324416

CREATE_A_TEAM_CHANNEL_ID = 1324440734836981912