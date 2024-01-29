# This example requires the 'message_content' intent.

import discord
from discord import app_commands
import cagematch_scraper

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return


@tree.command(
    name="suggestmatch", description="Suggest a match between two or more wrestlers!"
)
async def suggest_match(ctx, wrestlers: str, after_year: int, before_year: int, show_result: bool = False):
    try:
        print(show_result)
        await ctx.response.defer()
        wrestlers = wrestlers.split(",")
        print(wrestlers)
        print(after_year)
        print(before_year)
        wrestling_matches = cagematch_scraper.get_wrestling_matches(
            wrestlers, after_year, before_year
        )
        random_match = cagematch_scraper.pick_random_match(wrestling_matches)
        match_info = cagematch_scraper.extract_match_info(random_match, show_result)
        await ctx.followup.send(embed=match_embed(ctx, match_info))
    except Exception:
        await ctx.followup.send(
            embed=match_not_found_embed(ctx, wrestlers, after_year, before_year)
        )


def match_not_found_embed(ctx, wrestlers, after_year, before_year):
    wrestlers = ", ".join(wrestlers)
    embed = discord.Embed(
        title="Match Not Found",
        description=f"No match found that includes {wrestlers} between {before_year}-{after_year}. Make sure there are no typing errors or try broadening your search!",
        color=0xFF0000,
    )
    return embed


def match_embed(ctx, match):
    embed = discord.Embed(
        title=f"Match Suggestion for {ctx.user.display_name} ", description=match["match_details"], color=0xFFFF00
    )
    embed.add_field(name="Date", value=match["date"], inline=True)
    embed.add_field(name="Event", value=match["event"], inline=True)
    embed.add_field(name="Promotion", value=match["promotion"], inline=True)
    embed.set_thumbnail(url=match["image_link"])
    return embed


client.run("MTIwMTQ3MjA1NTA4Njk0MDI0MA.G0okY4.5bAHyA-g8vquiIxQw8sPOHoKewZhPk9pkigqUY")
