import discord
from discord.ext import commands

from discord import ui

from utils.database import *
from utils.config import *
from messages.your_scrim_message import get_your_scrim_message
from embeds.your_team_embed import get_your_team_embed


db = get_db_connection()

# Modal
class EditManualScrim(discord.ui.Modal, title="Edit Your Manual Scrim"):
    def __init__(self):
        super().__init__()

        self.scrim_date = discord.ui.TextInput(
            label="Date",
            placeholder="today",
            max_length=10
        )
        self.scrim_time = discord.ui.TextInput(
            label="Time",
            placeholder="now",
            max_length=10
        )
        self.scrim_best_of = discord.ui.TextInput(
            label="Best of / Duration",
            placeholder="bo7 / 1H",
            max_length=10
        )
        self.scrim_game_mode = discord.ui.TextInput(
            label="Game Mode",
            placeholder="3s",
            max_length=10
        )
        self.scrim_elo = discord.ui.TextInput(
            label="Elo",
            placeholder="2k2",
            max_length=10
        )

        self.add_item(self.scrim_date)
        self.add_item(self.scrim_time)
        self.add_item(self.scrim_best_of)
        self.add_item(self.scrim_game_mode)
        self.add_item(self.scrim_elo)

    async def on_submit(self, interaction: discord.Interaction):

        team = await get_team(interaction.user.id)

        team_id = team['id']

        await create_manual_scrim(team_id=team_id, date=self.scrim_date.value, time=self.scrim_time.value, best_of=self.scrim_best_of.value, game_mode=self.scrim_game_mode.value, elo=self.scrim_elo.value)

        scrim = await get_manual_scrim(team_id)

        message = await get_your_scrim_message(scrim)
        await interaction.response.send_message(
            message,
            ephemeral=True
        )

        message = await get_your_scrim_message(scrim)

        scrim_channel = bot.get_channel(SCRIM_CHANNEL_ID)

        scrim_search_channel = bot.get_channel(SCRIM_SEARCH_CHANNEL_ID)

        sent_message = await scrim_channel.send(message)

        await sent_message.publish()

        # await scrim_search_channel.send(message, view=)

