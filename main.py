import datetime
import os
import random
import logging

from patch import *

import discord
from discord import app_commands
from discord.ext import commands

from db.config import TOKEN, APP_ID, DB_CONFIG
from framework.utils import filter_deck_code, filter_account
from framework.mysql_db import MySQLDatabase
from framework.blizzard_website_api import BlizzardWebsiteAPI
from image_creator import ImageCreatorFunction

logger = logging.getLogger(__name__)
# configure basic logger in stream
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# init MySQLDatabase singleton
MySQLDatabase(DB_CONFIG)

client = commands.Bot(command_prefix="/",
                      application_id=APP_ID,
                      activity=discord.Game(name="Analyzing decks"),
                      intents=discord.Intents(43009))
                      #intents=discord.Intents.all())


async def generate_and_save(deck_code, function=ImageCreatorFunction.CREATE_DECK_PICTURE):
    image = await function(deck_code)

    if not image:
        return

    x, y = image.size
    image = image.resize((int(x / 1.2), int(y / 1.2)))

    name = random.randint(1000000, 10000000)

    image.save(f"{name}.png", format="PNG")

    return name


@client.event
async def on_ready():
    logger.info("Logged in as")
    logger.info(client.user.name)
    logger.info(client.user.id)
    logger.info(discord.__version__)
    logger.info("------")

    try:
        synced = await client.tree.sync()
        logger.info(f"synced {len(synced)} commands")
        logger.info("\n\n---------\n\n")
    except Exception as e:
        logger.error("sync error: %s" % e)

    logger.info("Servers connected to:")
    sum_servers, sum_members = 0, 0
    for guild in sorted(client.guilds, key=lambda cl: cl.member_count or 0):
        sum_servers += 1
        sum_members += guild.member_count or 0
        logger.info(f"{guild.name} - {guild.member_count} members")

    logger.info(f"ALL: {sum_servers} servers, {sum_members} members")
    logger.info("\n\n---------\n\n")


@client.tree.command(name="deck", description="Generates picture of deck by"
                                              'its code. Same as "/code"')
@app_commands.describe(deck_code="Generates picture of deck by its code."
                                 " May take a while")
async def deck(interaction: discord.Interaction, deck_code: str):
    await interaction.response.send_message("_En attente de la génération de l'image... "
                                            "Elle sera bientôt disponible_")
    deck_code = filter_deck_code(deck_code)
    if not deck_code:
        await interaction.edit_original_response(
            content=":face_with_spiral_eyes: Auncun code de deck trouvé dans le message.")
        return
    name = await generate_and_save(deck_code)

    if not name:
        await interaction.edit_original_response(
            content=":face_with_spiral_eyes: Erreur lors de la génération de l'image, veuillez réessayer.")
        return

    await interaction.edit_original_response(
        content=deck_code,
        attachments=[discord.File(f"{name}.png")]
    )

    os.remove(f"{name}.png")


@client.tree.command(name="code", description="Generates picture of deck by "
                                              'its code. Same as "/deck"')
@app_commands.describe(deck_code="Generates picture of deck by its code."
                                 " May take a while")
async def code(interaction: discord.Interaction, deck_code: str):
    await interaction.response.send_message("_En attente de la génération de l'image... "
                                            "Elle sera bientôt disponible_")
    deck_code = filter_deck_code(deck_code)
    if not deck_code:
        await interaction.edit_original_response(
            content=":face_with_spiral_eyes: Auncun code de deck trouvé dans le message.")
        return
    name = await generate_and_save(deck_code)

    if not name:
        await interaction.edit_original_response(
            content=":face_with_spiral_eyes: Erreur lors de la génération de l'image, veuillez réessayer.")
        return

    await interaction.edit_original_response(
        content=deck_code,
        attachments=[discord.File(f"{name}.png")]
    )

    os.remove(f"{name}.png")

@client.tree.command(name="rank", description="Get account rank")
@app_commands.describe(account="Get account rank")
async def rank(interaction: discord.Interaction, account: str):
    account = filter_account(account)
    if not await MySQLDatabase.instance.is_account_exist(account):
        await interaction.response.send_message(
            content=f":confounded: Le compte {account} n'est pas encore légende cette saison."
        )
        return
    await interaction.response.send_message("_En attente de la génération de l'image... "
                                            "Elle sera bientôt disponible_")
    # get account rank from database
    name = await generate_and_save(account, ImageCreatorFunction.CREATE_RANK_PICTURE)
    if not name:
        await interaction.edit_original_response(
            content=":face_with_spiral_eyes: Erreur lors de la génération de l'image, veuillez réessayer."
        )
        return
    await interaction.edit_original_response(
        content=f":trophy: Dernier classement de {account}:",
        attachments=[discord.File(f"{name}.png")])
    os.remove(f"{name}.png")
    
@client.tree.command(name="leaderboard", description="Get leaderboard info")
async def leaderboard(interaction: discord.Interaction):
    website_api = BlizzardWebsiteAPI()
    leaderboard_data = await website_api.get_leaderboard_data()
    if not leaderboard_data:
        await interaction.response.send_message(
            content="Une erreur est survenue lors de la recherche du classement des légendes. Veuillez reessayer plus tard."
            )
    rows = leaderboard_data.get("leaderboard", {}).get("rows", [])
    top = min(len(rows), 10)
    content = f"Top {top} des légendes de la saison:\n"
    for i in range(top):
        content += f"{rows[i]['rank']}: {rows[i]['accountid']}\n"
    content += f"Nombre total de légendes: {leaderboard_data.get('leaderboard', {}).get('pagination', {}).get('totalSize', 0)}"
    await interaction.response.send_message(content)

@client.command(name='deck')
async def deck(ctx, deck_code):
    name = await generate_and_save(deck_code)

    await ctx.send(file=discord.File(f"{name}.png"))

    os.remove(f"{name}.png")


@client.event
async def on_message(message: discord.message.Message):
    if message.author.bot:
        return
    text = message.content.split()

    start_time = datetime.datetime.now()

    for word in text:
        if word[:2] == "AA":
            ctx: discord.ext.commands.context.Context = \
                await client.get_context(message)

            name = await generate_and_save(word)

            await ctx.send(file=discord.File(f"{name}.png"))

            os.remove(f"{name}.png")

            logger.info(datetime.datetime.now() - start_time)


client.run(TOKEN)
