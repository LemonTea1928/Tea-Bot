import datetime
import typing

import discord
from discord.ext import commands


"""
Current time retriever
"""


def get_time() -> datetime.datetime:
    time_zone: datetime.timezone = datetime.timezone(
        offset=datetime.timedelta(hours=8),
        name="utc",
    )
    return datetime.datetime.now(tz=time_zone)


"""
Help embed creator
"""


def create_help_embed(
    bot: commands.Bot, command: typing.Optional[str] = None
) -> discord.Embed:
    help_embed: discord.Embed = discord.Embed(
        title="🍵 Tea Bot Command Helper 指令助手 :palm_up_hand:",
    )
    cmd_list: list = [cmd.name for cmd in bot.tree.walk_commands()]
    if not command:
        help_embed.add_field(
            name="📜 List of Tea Bot commands 指令列表",
            value="\n".join(
                [
                    str(index + 1) + ". " + cmd.name
                    for index, cmd in enumerate(bot.tree.walk_commands())
                ]
            ),
            inline=False,
        )
        help_embed.add_field(
            name="📔 Details 詳細內容",
            value="Type /help <Command Name> for command details\n"
            "輸入 /help <指令名稱> 取得該指令資訊",
            inline=False,
        )
    elif command in cmd_list:
        help_embed.add_field(
            name=command,
            value=bot.tree.get_command(command).description,
        )
    else:
        help_embed.add_field(
            name="🤔 Hmm... 嗯...",
            value="❌ I couldn't find this command! 我找不到這個指令！",
        )
    return help_embed


if __name__ == "__main__":
    pass
