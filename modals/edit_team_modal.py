import discord
from discord.ext import commands

from discord import ui

from utils.database import *
from embeds.your_team_embed import get_your_team_embed


db = get_db_connection()

# Modal
class EditTeam(discord.ui.Modal, title="Edit Your Team"):
    def __init__(self, name: str, description: str, elo: str):
        super().__init__()
        self.team_name = discord.ui.TextInput(
            label="Team Name",
            default=name,
            max_length=50
        )
        self.team_description = discord.ui.TextInput(
            label="Description",
            default=description,
            style=discord.TextStyle.long,
            max_length=200,
            required=False
        )
        self.team_elo = discord.ui.TextInput(
            label="Elo",
            default=elo,
            max_length=50
        )

        self.add_item(self.team_name)
        self.add_item(self.team_description)
        self.add_item(self.team_elo)

    async def on_submit(self, interaction: discord.Interaction):

        team = await get_team(interaction.user.id)

        await edit_team(team['id'], self.team_name.value, self.team_description.value, self.team_elo.value)

        team = await get_team(interaction.user.id)

        embed = await get_your_team_embed(team)
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

        channel = interaction.guild.get_channel(team['channel_id'])
        await channel.edit(name=team['name'])
        await channel.purge()

        await channel.send(embed=embed)
