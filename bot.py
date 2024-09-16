"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                Tea Bot - By nighttea_wf

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import core.GST as GST

import os
import asyncio
from json import loads
from pathlib import Path

import discord
from discord.ext import commands


intents: discord.Intents = discord.Intents.all()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix="Do ", intents=intents)


@bot.event
async def on_ready() -> None:
    """
    Display the bot's activity & status after initialization

    Returns:
        None
    """
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


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(
            token=loads(Path("credentials/token.json").read_text())["token"],
        )


if __name__ == "__main__":
    asyncio.run(main())
