import discord
from discord.ext import commands

from discord import ui

from utils.database import *
from utils.config import *
from messages.your_scrim_message import get_your_scrim_message
from embeds.your_team_embed import get_your_team_embed


db = get_db_connection()

# Modal
class EditAutoScrim(discord.ui.Modal, title="Edit Your Auto Scrim"):
    def __init__(self, date: str, time: str, best_of: str, game_mode: str, elo: str):
        super().__init__()

        self.scrim_date = date
        self.scrim_time = time
        self.scrim_best_of = best_of
        self.scrim_elo = elo
        self.scrim_game_mode = game_mode

        if self.scrim_date == None:
            self.scrim_date = discord.ui.TextInput(
                label="Date",
                placeholder="today",
                max_length=30
            )
        else:
            self.scrim_date = discord.ui.TextInput(
                label="Date",
                default=date,
                max_length=30
            )
        if self.scrim_time == None:
            self.scrim_time = discord.ui.TextInput(
                label="Time",
                placeholder="now",
                max_length=30
            )
        else:
            self.scrim_time = discord.ui.TextInput(
                label="Time",
                default=time,
                max_length=30
            )
        if self.scrim_best_of == None:
            self.scrim_best_of = discord.ui.TextInput(
                label="Best of / Duration",
                placeholder="bo7 / 1H",
                max_length=30
            )
        else:
            self.scrim_best_of = discord.ui.TextInput(
                label="Best of / Duration",
                default=best_of,
                max_length=30
            )
        if self.scrim_game_mode == None:
            self.scrim_game_mode = discord.ui.TextInput(
                label="Game Mode",
                placeholder="3s",
                max_length=30
            )
        else:
            self.scrim_game_mode = discord.ui.TextInput(
                label="Game Mode",
                default=game_mode,
                max_length=30
            )
        if self.scrim_elo == None:
            self.scrim_elo = discord.ui.TextInput(
                label="Elo",
                placeholder="2k2",
                max_length=30
            )
        else:
            self.scrim_elo = discord.ui.TextInput(
                label="Elo",
                default=elo,
                max_length=30
            )

        self.add_item(self.scrim_date)
        self.add_item(self.scrim_time)
        self.add_item(self.scrim_best_of)
        self.add_item(self.scrim_game_mode)
        self.add_item(self.scrim_elo)

    async def on_submit(self, interaction: discord.Interaction):

        team = await get_team(interaction.user.id)

        team_id = team['id']

        await edit_auto_scrim(team_id=team_id, date=self.scrim_date.value, time=self.scrim_time.value, best_of=self.scrim_best_of.value, game_mode=self.scrim_game_mode.value, elo=self.scrim_elo.value)

        scrim = await get_auto_scrim(team_id)

        if scrim is None:
            await create_auto_scrim(team_id=team_id, date=self.scrim_date.value, time=self.scrim_time.value, best_of=self.scrim_best_of.value, game_mode=self.scrim_game_mode.value, elo=self.scrim_elo.value)

        scrim = await get_auto_scrim(team_id)

        message = await get_your_scrim_message(scrim)
        await interaction.response.send_message(
            message,
            ephemeral=True
        )
