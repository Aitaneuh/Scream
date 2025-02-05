import discord

def get_team_utils_embed():
    embed = discord.Embed(
        title="Team Dashboard",
        description="By clicking the following buttons, you can interact with your team.",
        color=0xffa700
    )
    embed.add_field(
        name="Edit Team",
        value="Opens the form to modify your team settings.",
        inline=False
    )
    embed.add_field(
        name="See Your Team Presentation",
        value="Sends a message with your team information.",
        inline=False
    )
    embed.add_field(
        name="Edit Auto-Scrim",
        value="Opens the form to modify your auto-scrim settings.",
        inline=False
    )
    embed.add_field(
        name="See Your Auto-Scrim",
        value="Sends a preview of your scrim message.",
        inline=False
    )
    embed.add_field(
        name="Send Auto-Scrim",
        value="The bot will send a scrim request using the auto-scrim values.",
        inline=False
    )
    embed.add_field(
        name="Send Manual Scrim",
        value="Opens a form to manually configure and send a scrim request.",
        inline=False
    )
    embed.add_field(
        name="Kick a Player",
        value="Opens a menu to select and remove a team member.",
        inline=False
    )
    embed.add_field(
        name="Leave the Team",
        value="Leave the team but if you are the captain of it, the team will be deleted.",
        inline=False
    )
    embed.set_author(name="Written by Aitaneuh")
    embed.set_footer(text="Powered By Scream")

    return embed
