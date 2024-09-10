"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

To-do:
1. (Done) Ability to fetch and update giveaway message after bot restart
2. (Doing) Host bot
3. (Done) Allow only two players to click on Tic Tac Toe in each game session

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import core.GST as GST

import os
import asyncio
from json import loads
from pathlib import Path

import discord
from discord.ext import commands


"""
Bot initialization
"""
token: str = loads(Path("token.json").read_text())["token"]
intents: discord.Intents = discord.Intents.all()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix="Do ", intents=intents)


"""
Display the bot's activity & status after initialization
"""


@bot.event
async def on_ready() -> None:
    activity: discord.Activity = discord.Activity(
        type=discord.ActivityType.custom,
        name="custom",
        state="WIP 製作中",
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(
        "-------------------------\n"
        f"Logged in as {bot.user}\n"
        "-------------------------"
    )
    bot.add_view(GST.GSTButtonView())


"""
Command files loading, unloading & reloading
"""


@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.reply(f"Done loading {extension}.")


@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.reply(f"Done unloading {extension}.")


@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.reply(f"Done reloading {extension}.")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(token=token)


if __name__ == "__main__":
    asyncio.run(main())
