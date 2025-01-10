import discord
from discord.ui import Button, View

from utils.config import bot, SCRIM_CATEGORY_ID, SCRIM_REQUEST_CHANNEL_ID, GUILD_ID

from embeds.simple_embed import get_simple_embed
from embeds.scrim_decline_embed import get_scrim_decline_embed
from embeds.scrim_accept_embed import get_scrim_accept_embed
from embeds.new_scrim_embed import get_new_scrim_embed
from utils.database import create_scrim

class ScrimValidationButtons(View):
    def __init__(self, ask_team, scrim_team, scrim_message, message_id):
        super().__init__()
        self.ask_team = ask_team
        self.scrim_team = scrim_team
        self.scrim_message = scrim_message
        self.message_id = message_id

    @discord.ui.button(label="ACCEPT", style=discord.ButtonStyle.green, custom_id="accept")
    async def accept_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):
        scrim_request_channel = interaction.guild.get_channel(SCRIM_REQUEST_CHANNEL_ID)

        request_message = await scrim_request_channel.fetch_message(self.message_id)

        components = request_message.components
        new_components = []
        for action_row in components:
            new_row = discord.ui.ActionRow()
            for item in action_row.children:
                if isinstance(item, discord.ui.Button):
                    item.label = "CLOSE"
                    item.style = discord.ButtonStyle.gray
                    item.disabled = True
                new_row.append_item(item)
            new_components.append(new_row)

        await request_message.edit(components=new_components)


        captain_id = self.ask_team['captain_id']

        captain = await bot.fetch_user(captain_id)

        category = discord.utils.get(interaction.guild.categories, id=SCRIM_CATEGORY_ID)

        guild = bot.get_guild(GUILD_ID)

        team_host_role = guild.get_role(self.scrim_team['role_id'])
        team_request_role = guild.get_role(self.ask_team['role_id'])

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            team_host_role: discord.PermissionOverwrite(view_channel=True),
            team_request_role: discord.PermissionOverwrite(view_channel=True)
        }

        scrim_channel = await interaction.guild.create_text_channel(f"{self.scrim_team['name']} vs {self.ask_team['name']}", category=category, overwrites=overwrites)

        await create_scrim(message_id=self.message_id, team_host_id=self.scrim_team['id'], team_request_id=self.ask_team['id'], scrim_channel_id=scrim_channel.id)

        new_scrim_embed = get_new_scrim_embed(team_host=self.scrim_team, team_request=self.ask_team)

        await scrim_channel.send(embed=new_scrim_embed)

        accept_embed = get_scrim_accept_embed(host_team=self.scrim_team, scrim_message=self.scrim_message, scrim_channel_id=scrim_channel.id)
        await captain.send(embed=accept_embed)

        confirmation_embed = get_simple_embed("This scrim request has been succesfully accepted.")

        await interaction.response.send_message(embed=confirmation_embed, ephemeral=True)


    @discord.ui.button(label="DECLINE", style=discord.ButtonStyle.red, custom_id="decline")
    async def decline_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):
        captain_id = self.ask_team['captain_id']

        captain = await bot.fetch_user(captain_id)

        decline_embed = get_scrim_decline_embed(host_team=self.scrim_team, scrim_message=self.scrim_message)
        await captain.send(embed=decline_embed)

        confirmation_embed = get_simple_embed("This scrim request has been succesfully declined.")
        await interaction.message.delete()
        await interaction.response.send_message(embed=confirmation_embed, ephemeral=True)