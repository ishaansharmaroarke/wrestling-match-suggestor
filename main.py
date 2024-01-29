# This example requires the 'message_content' intent.

import discord
from discord import app_commands
import cagematch_scraper
import os
from dotenv import load_dotenv
import datetime
import traceback

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
    description="Suggest a match involving one or more wrestlers! (Use full-names and commas to upto 4 wrestlers)",
)
async def suggest_match(
    ctx,
    wrestlers: str,
    after_year: int,
    before_year: int = datetime.datetime.now().year,
):
    try:
        await ctx.response.defer()
        wrestlers = wrestlers.split(",")
        wrestling_matches = cagematch_scraper.get_wrestling_matches(
            wrestlers, after_year, before_year
        )
        random_match = cagematch_scraper.pick_random_match(wrestling_matches)
        match_info = cagematch_scraper.extract_match_info(random_match)
        await ctx.followup.send(embed=match_embed(ctx, match_info))
    except Exception as e:
        error_message = f"An error occurred: {str(e)}\n\n{traceback.format_exc()}"
        with open("error.log", "a") as file:
            file.write(error_message)

        await ctx.followup.send(
            embed=match_not_found_embed(ctx, wrestlers, after_year, before_year)
        )


def match_not_found_embed(ctx, wrestlers, after_year, before_year):
    wrestlers = ", ".join(wrestlers)
    embed = discord.Embed(
        title="Match Not Found",
        description=f"No match found that includes {wrestlers} between {after_year}-{before_year}. Make sure there are no typing errors or try broadening your search! (if you're trying to search for more than one wrestler, make sure you use only commas to separate them)",
        color=0xFF0000,
    )
    return embed


def match_embed(ctx, match):
    description = f"{match['match_type']} {match['match_details']}" 
    embed = discord.Embed(
        title=f"Match Suggestion for {ctx.user.display_name}",
        description=description,
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
