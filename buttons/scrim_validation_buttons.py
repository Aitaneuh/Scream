import discord
from discord.ui import Button, View

from utils.config import bot

from embeds.simple_embed import get_simple_embed
from embeds.scrim_decline_embed import get_scrim_decline_embed

class ScrimValidationButtons(View):
    def __init__(self, ask_team, scrim_team, scrim_message):
        super().__init__()
        self.ask_team = ask_team
        self.scrim_team = scrim_team
        self.scrim_message = scrim_message

    @discord.ui.button(label="ACCEPT", style=discord.ButtonStyle.green, custom_id="accept")
    async def accept_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):
        return

    @discord.ui.button(label="DECLINE", style=discord.ButtonStyle.red, custom_id="decline")
    async def decline_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):
        captain_id = self.ask_team['captain_id']

        captain = await bot.fetch_user(captain_id)

        decline_embed = get_scrim_decline_embed(host_team=self.scrim_team, scrim_message=self.scrim_message)
        await captain.send(embed=decline_embed)

        confirmation_embed = get_simple_embed("This scrim request has been succesfully declined.")
        await interaction.message.delete()
        await interaction.response.send_message(embed=confirmation_embed, ephemeral=True)