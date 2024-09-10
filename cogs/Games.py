"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                    Cog - Games extension

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import core.TTT as TTT
import core.classes as classes

import discord
from discord import app_commands
from discord.ext import commands


class Games(classes.Cog_Extension):
    ttt_sessions: list = [{session_id: 0} for session_id in range(1, 11)]

    # TicTacToe (TTT)
    @app_commands.command(
        name="tictactoe",
        description="Launch the Tic Tac Toe game 開啟井字過三關遊戲",
    )
    async def tictactoe(self, cmd_interaction: discord.Interaction) -> None:
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


async def setup(bot: commands.Bot):
    await bot.add_cog(Games(bot))


if __name__ == "__main__":
    pass
