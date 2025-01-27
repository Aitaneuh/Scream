import discord
from discord.ext import commands

from discord import ui

from utils.database import *
from utils.config import *
from embeds.your_team_embed import get_your_team_embed


db = get_db_connection()

# Modal
class CreateTeam(discord.ui.Modal, title="Edit Your Team"):
    def __init__(self):
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

        player_role = discord.utils.get(interaction.guild.roles, id=PLAYER_ROLE_ID)

        await interaction.user.add_roles(player_role)

        await create_team(interaction.user.id, self.team_name.value, self.team_description.value, self.team_elo.value)

        team = await get_team(interaction.user.id)

        embed = await get_your_team_embed(team)
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

        category = discord.utils.get(interaction.guild.categories, id=TEAM_PROFILES_ID)

        channel = await interaction.guild.create_text_channel(team['name'], category=category)

        await add_channel_id(team_id=team['id'], channel_id=channel.id)

        team_role = await interaction.guild.create_role(name=team['name'])

        await add_role_id(team_id=team['id'], role_id=team_role.id)

        await interaction.user.add_roles(team_role)

        embed = await get_your_team_embed(team)
        await channel.send(embed=embed)
