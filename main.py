import datetime
import os
import random
import base64

from patch import *

import discord
from discord import app_commands
from discord.ext import commands

from db.config import TOKEN, APP_ID, DB_CONFIG
from framework.local_db import MySQLDatabase
from image_creator import create_picture

client = commands.Bot(command_prefix="/",
                      application_id=APP_ID,
                      activity=discord.Game(name="Analyzing decks"),
                      intents=discord.Intents(43008))
                      #intents=discord.Intents.all())


async def filter_deck_code(deck_code):
    # iterate on deck_code as word separated by space to find a base64 code starting with AA
    for word in deck_code.split():
        if word[:2] == "AA":
            try:
                base64.b64decode(word)
            except:
                continue
            return word

async def generate_and_save(deck_code):
    image = await create_picture(deck_code)

    if not image:
        return

    x, y = image.size
    image = image.resize((int(x / 1.2), int(y / 1.2)))

    name = random.randint(1000000, 10000000)

    image.save(f"{name}.png", format="PNG")

    return name


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print(discord.__version__)
    print("------")

    client.db = MySQLDatabase(DB_CONFIG)

    try:
        synced = await client.tree.sync()
        print(f"synced {len(synced)} commands")
        print("\n\n---------\n\n")
    except Exception as e:
        print("sync error:", e)

    print("Servers connected to:")
    sum_servers, sum_members = 0, 0
    print(f"test:{client.guilds}")
    for guild in sorted(client.guilds, key=lambda cl: cl.member_count or 0):
        sum_servers += 1
        sum_members += guild.member_count or 0
        print(guild.name, "-----", guild.member_count, "members")

    print(f"ALL: {sum_servers} servers, {sum_members} members")
    print("\n\n---------\n\n")


@client.tree.command(name="deck", description="Generates picture of deck by"
                                              'its code. Same as "/code"')
@app_commands.describe(deck_code="Generates picture of deck by its code."
                                 " May take a while")
async def deck(interaction: discord.Interaction, deck_code: str):
    await interaction.response.send_message("_En attente de la génération de l'image... "
                                            "Elle sera bientôt disponible_")
    deck_code = await filter_deck_code(deck_code)
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
    deck_code = await filter_deck_code(deck_code)
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
    # get account rank from database
    rank = await client.db.get_last_rank(account)
    if rank is None:
        await interaction.response.send_message(f"Compte {account} non trouvé dans la base de données.")
    else:
        await interaction.response.send_message(f":trophy: Dernier classement connu de {account}: {rank}")
    

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

            print(datetime.datetime.now() - start_time)


client.run(TOKEN)
