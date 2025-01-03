import discord
from discord.ext import commands

from discord import ui

from utils.database import *
from embeds.your_team import get_your_team_embed


db = get_db_connection()

class EmbedBuilder(discord.ui.View):
    def __init__(self, userid, embed : discord.Embed):
        super().__init__(timeout=None)
        self.userid = userid
        self.embed = embed

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.blurple, custom_id="edit_button")
    async def edit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = CreateTeam(self.userid, self.embed)
        await interaction.response.send_modal(modal)


# Modal
class CreateTeam(discord.ui.Modal, title="Edit Your Team"):
    def __init__(self, name: str, description: str, elo: str):
        super().__init__()
        self.team_name = discord.ui.TextInput(
            label="Team Name",
            placeholder="Your team name here",
            max_length=50
        )
        self.team_description = discord.ui.TextInput(
            label="Description",
            placeholder="Your team's description here (can be empty)",
            style=discord.TextStyle.long,
            max_length=200,
            required=False
        )
        self.team_elo = discord.ui.TextInput(
            label="Elo",
            placeholder="2100",
            max_length=50
        )

        self.add_item(self.team_name)
        self.add_item(self.team_description)
        self.add_item(self.team_elo)

    async def on_submit(self, interaction: discord.Interaction):

        await create_team(interaction.user.id, self.team_name.value, self.team_description.value, self.team_elo.value)

        team = await get_team(interaction.user.id)

        embed = await get_your_team_embed(team)
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
