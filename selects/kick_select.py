import discord

from embeds.simple_embed import get_simple_embed
from utils.database import db_leave_team
from utils.config import bot


class KickSelect(discord.ui.View):
    def __init__(self, captain_id: int, members: list):
        super().__init__()
        self.captain_id = captain_id

        options = [
            discord.SelectOption(label=f"{member[1]}", value=str(member[0])) for member in members
        ]

        self.select = discord.ui.Select(placeholder="Choose a player to kick", options=options)
        self.select.callback = self.kick_player
        self.add_item(self.select)

    async def kick_player(self, interaction: discord.Interaction):
        player_id = int(self.select.values[0])

        await db_leave_team(player_id)

        player = bot.fetch_user(player_id)

        kick_player_embed = get_simple_embed(f"The player {player.display_name} has been kicked.")
        await interaction.response.send_message(embed=kick_player_embed)
        self.stop()