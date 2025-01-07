import discord
from discord.ui import Button, View

from utils.database import *
from utils.config import bot
from embeds.scrim_request_embed import get_scrim_request_embed
from embeds.simple_embed import get_simple_embed
from messages.small_scrim_message import get_small_scrim_message
from buttons.scrim_validation_buttons import ScrimValidationButtons

class TakeScrimButton(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="OPEN", style=discord.ButtonStyle.green, custom_id="take_scrim")
    async def take_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):
        message_id = interaction.message.id

        ask_team = await get_team(interaction.user.id)

        ask_team_member_ids = await get_team_members(ask_team['id'])

        #if len(ask_team_member_ids) < 3:
            #at_least_embed = get_simple_embed("You have to be at least 3 in your team to play scrims.")
            #await interaction.response.send_message(embed=at_least_embed, ephemeral=True)
            #return

        scrim_team = await get_team_from_message_id(message_id)

        #if scrim_team == ask_team:
            #same_team_embed = get_simple_embed("You can't scrim against your own team.")
            #await interaction.response.send_message(embed=same_team_embed, ephemeral=True)
            #return

        captain_id = scrim_team['captain_id']

        captain = await bot.fetch_user(captain_id)

        roster = ""

        for player_id in ask_team_member_ids:
            player = await bot.fetch_user(player_id)
            roster += f"{player.mention} "

        scrim = await get_scrim_from_message_id(message_id)

        scrim_message = await get_small_scrim_message(scrim)

        final_embed = get_scrim_request_embed(ask_team, roster, scrim_message)

        await captain.send(embed=final_embed, view=ScrimValidationButtons(ask_team=ask_team, scrim_message=scrim_message, scrim_team=scrim_team))

        message_sent_embed = get_simple_embed(f"A request have been send to {captain.mention}, the captain of {scrim_team['name']}.")

        await interaction.response.send_message(embed=message_sent_embed, ephemeral=True)