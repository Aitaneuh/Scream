from discord.ext import commands
from utils.database import create_tables

async def on_lunch(bot: commands.Bot):
    await create_tables()
    print("Bot is online ! ", "| Name :", bot.user.name, "| ID :", bot.user.id)
