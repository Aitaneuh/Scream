import discord
from discord.ext import commands

from discord import ui

from utils.database import *
from utils.config import *
from buttons.scrim_take_button import *
from messages.your_scrim_message import get_your_scrim_message


db = get_db_connection()

# Modal
class SendManualScrim(discord.ui.Modal, title="Send Your Manual Scrim"):
    def __init__(self):
        super().__init__()

        self.scrim_date = discord.ui.TextInput(
            label="Date",
            placeholder="today",
            max_length=30
        )
        self.scrim_time = discord.ui.TextInput(
            label="Time",
            placeholder="now",
            max_length=30
        )
        self.scrim_best_of = discord.ui.TextInput(
            label="Best of / Duration",
            placeholder="bo7 / 1H",
            max_length=30
        )
        self.scrim_game_mode = discord.ui.TextInput(
            label="Game Mode",
            placeholder="3s",
            max_length=30
        )
        self.scrim_elo = discord.ui.TextInput(
            label="Elo",
            placeholder="2k2",
            max_length=30
        )

        self.add_item(self.scrim_date)
        self.add_item(self.scrim_time)
        self.add_item(self.scrim_best_of)
        self.add_item(self.scrim_game_mode)
        self.add_item(self.scrim_elo)

    async def on_submit(self, interaction: discord.Interaction):

        team = await get_team(interaction.user.id)

        team_member_ids = await get_team_members(team['id'])

        #if len(team_member_ids) < 3:
            #at_least_embed = get_simple_embed("You have to be at least 3 in your team to play scrims.")
            #await interaction.response.send_message(embed=at_least_embed, ephemeral=True)
            #return

        team_id = team['id']

        await create_manual_scrim(team_id=team_id, date=self.scrim_date.value, time=self.scrim_time.value, best_of=self.scrim_best_of.value, game_mode=self.scrim_game_mode.value, elo=self.scrim_elo.value)

        scrim = await get_manual_scrim(team_id)

        message = await get_your_scrim_message(scrim)
        await interaction.response.send_message(
            message,
            ephemeral=True
        )

        message = await get_your_scrim_message(scrim)

        announcement_channel = bot.get_channel(ANNOUNCEMENT_CHANNEL_ID)

        pick_channel = bot.get_channel(PICK_CHANNEL_ID)

        announcement_message = await announcement_channel.send(message)

        await announcement_message.publish()

        pick_message = await pick_channel.send(message, view=TakeScrimButton())

        await add_manual_message_id(team_id=team_id, announcement_message_id=announcement_message.id, pick_message_id=pick_message.id)

        await interaction.response.send_message(f"Your scrim request have been sended\n\nIn scrims channel : https://discord.com/channels/{interaction.guild.id}/{ANNOUNCEMENT_CHANNEL_ID}/{announcement_message.id}\n\nIn scrims search channel : https://discord.com/channels/{interaction.guild.id}/{PICK_CHANNEL_ID}/{pick_message.id}", ephemeral=True)

