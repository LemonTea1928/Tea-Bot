"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                    Cog - Utils extension

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
import typing

import core.functions as functions
import core.classes as classes
import bot

import discord
from discord import app_commands
from discord.ext import commands


class Utils(classes.Cog_Extension):
    """
    Cog extension class for various server utilities

    Attributes:
        extension_list (list): All cog extensions for displaying in command

    Methods:
        load: Load a cog extension
        unload: Unload a cog extension
        reload: Reload a cog extension
        giveaway: Launch GST GUI
        sync: Sync slash (app) commands
        help: Slash command replacement for the text counterpart
    """
    extension_list: list = [
        app_commands.Choice(name=filename[:-3], value=index)
        for index, filename in enumerate(os.listdir("./cogs"))
        if filename.endswith(".py")
    ]

    @app_commands.command(
        name="load",
        description="Load cogs extension 載入cogs附加元件",
    )
    @app_commands.choices(extensions=extension_list)
    async def load(
        self,
        interaction: discord.Interaction,
        extensions: app_commands.Choice[int],
    ) -> None:
        await self.bot.load_extension(f"cogs.{extensions.name}")
        await interaction.response.send_message(
            content=f"Loaded 已載入 {extensions.name}",
            ephemeral=True,
        )

    @app_commands.command(
        name="unload",
        description="Unload cogs extension 卸載cogs附加元件",
    )
    @app_commands.choices(extensions=extension_list)
    async def unload(
        self,
        interaction: discord.Interaction,
        extensions: app_commands.Choice[int],
    ) -> None:
        await self.bot.unload_extension(f"cogs.{extensions.name}")
        await interaction.response.send_message(
            content=f"Unloaded 已卸載 {extensions.name}",
            ephemeral=True,
        )

    @app_commands.command(
        name="reload",
        description="Reload cogs extension 重新載入cogs附加元件",
    )
    @app_commands.choices(extensions=extension_list)
    async def reload(
        self,
        interaction: discord.Interaction,
        extensions: app_commands.Choice[int],
    ) -> None:
        await self.bot.reload_extension(f"cogs.{extensions.name}")
        await interaction.response.send_message(
            content=f"Reloaded 已重新載入 {extensions.name}",
            ephemeral=True,
        )

    @app_commands.command(
        name="sync",
        description="Sync commands 同步指令",
    )
    async def sync(self, interaction: discord.Interaction) -> None:
        await self.bot.tree.sync()
        await interaction.response.send_message(
            content="Commands synced.",
            ephemeral=True,
        )

    @app_commands.command(
        name="help",
        description="Show available bot commands 檢視可用的bot指令",
    )
    @app_commands.choices(command=[cmd.name for cmd in bot.bot.tree.walk_commands()])
    async def help(
        self,
        interaction: discord.Interaction,
        command: typing.Optional[str] = None,
    ) -> None:
        embed = functions.create_help_embed(self.bot, command)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(
        name="usage",
        description="Show bot's system usage 檢視bot的系統資源使用率",
    )
    async def usage(
        self,
        interaction: discord.Interaction,
    ) -> None:
        embed = functions.create_usage_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot))


if __name__ == "__main__":
    pass
