import core.GST as GST
import core.classes as classes

import discord
from discord import app_commands
from discord.ext import commands


class Giveaway(classes.Cog_Extension):
    giveaway_command_group = app_commands.Group(
        name="giveaway",
        description="Giveaway-related commands 抽獎活動相關指令",
    )

    def __init__(self, bot) -> None:
        super().__init__(bot)


    @giveaway_command_group.command(
        name="create",
        description="Launch the Giveaway Setup Tool 開啟抽獎工具",
    )
    async def create(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(GST.GUI())


    @giveaway_command_group.command(
        name="listall",
        description="List all active giveaways 顯示所有進行中的抽獎活動",
    )
    async def listall(self, interaction: discord.Interaction) -> None:
        embed: discord.Embed = GST.create_listall_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Giveaway(bot))


if __name__ == '__main__':
    pass