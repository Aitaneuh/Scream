from discord.ext import commands
from utils.database import create_tables
from messages.on_ready_messages import send_messages

async def on_lunch(bot: commands.Bot):
    await create_tables()
    await send_messages()
    print("Bot is online ! ", "| Name :", bot.user.name, "| ID :", bot.user.id)
