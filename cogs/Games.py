"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                    Cog - Games extension

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import core.classes as classes
import core.TTT as TTT
import core.Wordle as Wordle

import discord
from discord import app_commands
from discord.ext import commands


class Games(classes.Cog_Extension):
    """
    Cog extension for loading games as Discord messages

    Attributes:
        ttt_sessions (list[dict]): Available Tic Tac Toe sessions (max. 10)
    
    Methods:
        tictactoe: Launch TTT game
    """
    ttt_sessions: list[dict] = [{session_id: 0} for session_id in range(1, 11)]

    @app_commands.command(
        name="tictactoe",
        description="Launch the Tic Tac Toe game 開啟井字過三關遊戲",
    )
    async def tictactoe(self, cmd_interaction: discord.Interaction) -> None:
        """
        Launch the Tic Tac Toe game (if available)
        
        1.  If all game sessions are occupied, prompt the user to check later
        2.  If there is an available session then allocate one. Free up the
            session after no interactions on the PlayerSelectButton for
            5 seconds (TTT.py)

        Returns:
            None
        """
        if all([Dict.get(i + 1) for i, Dict in enumerate(self.ttt_sessions)]):
            await cmd_interaction.response.send_message(
                content="❗ All sessions are currently full! "
                "Please check again later.\n"
                "❗ 所有遊戲皆已滿額！請在稍後再來。",
                ephemeral=True,
            )
            return

        session_id: int = TTT.session_id_assign(self.ttt_sessions)
        await cmd_interaction.response.send_message(
            content="Choose O or X to play. "
            "The game starts after two players have joined.\n"
            "請選擇 O 或 X 遊玩。遊戲會在兩名玩家加入後開始。",
            view=TTT.PlayerSelectButton(
                cmd_interaction=cmd_interaction,
                session_id=session_id,
            ),
        )
    
    @app_commands.command(
        name="wordle",
        description="Launch the Wordle game 開啟 Wordle 猜字遊戲",
    )
    async def wordle(self, cmd_interaction: discord.Interaction) -> None:
        await cmd_interaction.response.send_message(
            content="🤔 Wordle!",
            view=Wordle.StartView(cmd_interaction),
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))


if __name__ == "__main__":
    pass
