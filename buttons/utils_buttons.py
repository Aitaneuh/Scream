import discord
from discord.ui import Button, View

from embeds.your_team_embed import get_your_team_embed
from embeds.simple_embed import get_simple_embed
from utils.database import *
from utils.config import *
from modals.edit_team_modal import EditTeam
from modals.edit_auto_scrim import EditAutoScrim
from modals.send_manual_scrim import SendManualScrim
from messages.your_scrim_message import get_your_scrim_message
from buttons.scrim_take_button import TakeScrimButton

class UtilsButtons(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Edit Your Team", style=discord.ButtonStyle.green, custom_id="edit_your_team")
    async def edit_team(self, interaction: discord.Interaction, button: discord.ui.Button):

        team = await get_team(interaction.user.id)

        if team == None:
            await interaction.response.send_message(f"You are not part of a team", ephemeral=True)
        else:
            await interaction.response.send_modal(EditTeam(name=team['name'], description=team['description'], elo=team['elo']))

    @discord.ui.button(label="See Your Team Presentation", style=discord.ButtonStyle.blurple, custom_id="see_your_team")
    async def see_team(self, interaction: discord.Interaction, button: discord.ui.Button):

        team = await get_team(interaction.user.id)

        if team == None:
            await interaction.response.send_message(f"You are not part of a team", ephemeral=True)
        else:
            embed = await get_your_team_embed(team)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Edit Auto-Scrim", style=discord.ButtonStyle.green, custom_id="edit_auto_scrim")
    async def edit_auto_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):

        team = await get_team(interaction.user.id)

        team_id = team['id']

        scrim = await get_auto_scrim(team_id)

        if scrim == None:
            await interaction.response.send_modal(EditAutoScrim(date=None, time=None, best_of=None, elo=None, game_mode=None))
        else:
            await interaction.response.send_modal(EditAutoScrim(date=scrim['date'], time=scrim['time'], best_of=scrim['best_of'], elo=scrim['elo'], game_mode=scrim['game_mode']))

    @discord.ui.button(label="See Your Auto-Scrim", style=discord.ButtonStyle.blurple, custom_id="see_your_auto_scrim")
    async def see_auto_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):

        team = await get_team(interaction.user.id)

        team_id = team['id']

        scrim = await get_auto_scrim(team_id)

        if scrim == None:
            await interaction.response.send_message(f"Auto scrim is not setup in your team", ephemeral=True)
        else:
            message = await get_your_scrim_message(scrim)
            await interaction.response.send_message(
                message,
                ephemeral=True
            )

    @discord.ui.button(label="Send Auto-Scrim", style=discord.ButtonStyle.red, custom_id="send_auto_scrim")
    async def send_auto_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):

        team = await get_team(interaction.user.id)

        team_id = team['id']

        team_member_ids = await get_team_members(team_id)

        #if len(team_member_ids) < 3:
            #at_least_embed = get_simple_embed("You have to be at least 3 in your team to play scrims.")
            #await interaction.response.send_message(embed=at_least_embed, ephemeral=True)
            #return

        scrim = await get_auto_scrim(team_id)

        if scrim == None:
            await interaction.response.send_message(f"Auto scrim is not setup in your team", ephemeral=True)
        else:
            message = await get_your_scrim_message(scrim)

            announcement_channel = bot.get_channel(ANNOUNCEMENT_CHANNEL_ID)

            pick_channel = bot.get_channel(PICK_CHANNEL_ID)

            announcement_message = await announcement_channel.send(message)

            await announcement_message.publish()

            pick_message = await pick_channel.send(message, view=TakeScrimButton())

            await add_auto_message_id(team_id=team_id, announcement_message_id=announcement_message.id, pick_message_id=pick_message.id)

            await interaction.response.send_message(f"Your scrim request have been send\n\nIn scrims channel : https://discord.com/channels/{interaction.guild.id}/{ANNOUNCEMENT_CHANNEL_ID}/{announcement_message.id}\n\nIn scrims search channel : https://discord.com/channels/{interaction.guild.id}/{PICK_CHANNEL_ID}/{pick_message.id}", ephemeral=True)


    @discord.ui.button(label="Send Manual Scrim", style=discord.ButtonStyle.red, custom_id="send_manual_scrim")
    async def send_manual_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_modal(SendManualScrim())