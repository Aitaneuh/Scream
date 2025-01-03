import discord
from discord.ui import Button, View

from embeds.your_team import get_your_team_embed
from embeds.simple_embed import get_simple_embed
from utils.database import *
from modals.create_team_modal import CreateTeam

class TeamButtons(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Create Your Team", style=discord.ButtonStyle.green, custom_id="create_a_team")
    async def create_team(self, interaction: discord.Interaction, button: discord.ui.Button):

        team = await get_team(interaction.user.id)

        if team == None:
            await interaction.response.send_modal(CreateTeam(name=None, description=None, elo=None))
        else:
            await interaction.response.send_message(f"You are already part of a team : {team['name']}", ephemeral=True)


