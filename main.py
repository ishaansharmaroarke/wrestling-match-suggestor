# This example requires the 'message_content' intent.

import discord
from discord import app_commands
import cagematch_scraper
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

load_dotenv()
token = os.getenv("BOT_TOKEN")


@client.event
async def on_ready():
    await tree.sync()
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return


@tree.command(
    name="suggestmatch",
    description="Suggest a match involving one or more wrestlers! (Upto 4 only)",
)
async def suggest_match(
    ctx,
    wrestlers: str,
    after_year: int,
    before_year: int = 2024,
    show_result: bool = False,
):
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
            embed=match_not_found_embed(ctx, wrestlers, after_year, before_year=2024)
        )


def match_not_found_embed(ctx, wrestlers, after_year, before_year):
    wrestlers = ", ".join(wrestlers)
    embed = discord.Embed(
        title="Match Not Found",
        description=f"No match found that includes {wrestlers} between {after_year}-{before_year}. Make sure there are no typing errors or try broadening your search!",
        color=0xFF0000,
    )
    return embed


def match_embed(ctx, match):
    embed = discord.Embed(
        title=f"Match Suggestion for {ctx.user.display_name} ",
        description=match["match_details"],
        color=0xFFFF00,
    )
    embed.add_field(name="Date", value=match["date"], inline=True)
    embed.add_field(name="Event", value=match["event"], inline=True)
    embed.add_field(name="Promotion", value=match["promotion"], inline=True)
    embed.add_field(name="Winner", value=f"||{match['result']}||", inline=True)
    embed.set_footer(
        text="Powered by CageMatch.net",
        icon_url="https://cdn.discordapp.com/attachments/1201470152739389452/1201558708640030862/cagematch.jpg",
    )
    embed.set_thumbnail(url=match["image_link"])
    return embed


client.run(token)
