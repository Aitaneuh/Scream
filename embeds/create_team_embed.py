import discord

def get_create_team_embed():
    embed = discord.Embed(
    title=f"How to create YOUR scream team ?",
    description="Follow this step-by-step guide to get your team up and running.",
    color=0xff005a
    )
    embed.add_field(
        name="Step 1: Click the 'Create Your Team' Button",
        value="The first step is simple! Click the **Create Your Team** button below this message to start.",
        inline=False
    )
    embed.add_field(
        name="Step 2: Team Profile Example",
        value="Next, the bot will send you an example of a team profile via private message.",
        inline=False
    )
    embed.add_field(
        name="Step 3: Fill in Your Team Information",
        value="The bot will ask you for information such as your team's **name**, **description**, and an **indicative elo**.",
        inline=False
    )
    embed.add_field(
        name="Step 4: Validate Your Team",
        value="Once you've filled everything out, click the **Validate** button to officially create your team. You will automatically become the **captain** of the team.",
        inline=False
    )
    embed.set_author(name="Written by Aitaneuh")
    embed.set_footer(text="Powered By Scream")

    return embed