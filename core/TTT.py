"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                    Tic Tac Toe (TTT) 
                            (Adapted from discord.py example)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import cogs.Games as Games

from typing import List

import discord


def session_id_assign(ttt_sessions: dict) -> int:
    for i, Dict in enumerate(ttt_sessions):
        if Dict.get(i + 1) == 0: return i + 1


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int, session_id: int, o_id: int, x_id: int) -> None:
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label="\u200b",
            row=y,
        )
        self.x = x
        self.y = y
        self.o_id: int = o_id
        self.x_id: int = x_id
        self.session_id: int = session_id
        self.id_list: list[int] = [o_id, x_id]

    async def callback(self, interaction: discord.Interaction) -> None:
        self.interaction: discord.Interaction = interaction
        if interaction.user.id not in self.id_list:
            await interaction.response.send_message(
                content="❗ You can't play in this session!\n❗ 你不能玩這場遊戲！",
                ephemeral=True,
            )
            return

        assert self.view is not None
        view: TicTacToe = self.view
        state: int = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if (view.current_player == view.X) and (interaction.user.id == self.x_id):
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"(ID: {self.session_id}) Now it's O's turn 現在是 O 的回合"
            delete_after = None

        elif (view.current_player == view.O) and (interaction.user.id == self.o_id):
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"(ID: {self.session_id}) Now it's X's turn 現在是 X 的回合"
            delete_after = None

        else:
            await interaction.response.send_message(
                content="❗ You can't impersonate others!\n❗ 你不能冒充其他人！",
                ephemeral=True,
            )
            return

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f"(ID: {self.session_id}) X won! X 贏了！"
                delete_after: float = 5.0
            elif winner == view.O:
                content = f"(ID: {self.session_id}) O won! O 贏了！"
                delete_after: float = 5.0
            else:
                content = f"(ID: {self.session_id}) Tie! 平手！"
                delete_after: float = 5.0

            for child in view.children:
                child.disabled = True

            view.stop()

            Games.Games.ttt_sessions[self.session_id - 1].update({self.session_id: 0})

        await interaction.response.edit_message(
            content=content,
            view=view,
            delete_after=delete_after,
        )


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X: int = -1
    O: int = 1
    Tie: int = 2

    def __init__(self, session_id: int, o_id: int, x_id: int) -> None:
        super().__init__()
        self.session_id: int = session_id
        self.current_player = self.X
        self.o_id: int = o_id
        self.x_id: int = x_id
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y, session_id, o_id, x_id))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        if diag == -3:
            return self.X

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class PlayerSelectButton(discord.ui.View):
    def __init__(
        self,
        cmd_interaction: discord.Interaction,
        session_id: int,
    ) -> None:
        super().__init__(timeout=5.0)
        self.cmd_interaction: discord.Interaction = cmd_interaction
        self.checklist: list[bool] = [False, False]
        self.session_id: int = session_id
        self.o_id: int = 0
        self.x_id: int = 1

    async def global_callback(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        match interaction.data['custom_id']:
            case 'buttonO': self.checklist[0] = True
            case 'buttonX': self.checklist[1] = True
        button.disabled = True
        await interaction.response.edit_message(view=self)
        
        if all(self.checklist):
            self.timeout = None
            Games.Games.ttt_sessions[self.session_id - 1].update(
                {self.session_id: (self.o_id, self.x_id)},
            )
            await self.cmd_interaction.edit_original_response(
                content=f"(ID:{self.session_id}) "
                "Tic Tac Toe! X goes first 過三關！X 先開始",
                view=TicTacToe(self.session_id, self.o_id, self.x_id),
            )

    @discord.ui.button(
        label="O",
        style=discord.ButtonStyle.success,
        custom_id="buttonO",
    )
    async def button_o_callback(
        self,
        interaction_o: discord.Interaction,
        button_o: discord.ui.Button,
    ) -> None:
        self.o_id: int = interaction_o.user.id
        if self.o_id == self.x_id:
            await interaction_o.response.send_message(
                content="❌ You cannot impersonate others! 你不能冒充其他人！❌",
                ephemeral=True,
            )
            return
        await self.global_callback(interaction_o, button_o)

    @discord.ui.button(
        label="X",
        style=discord.ButtonStyle.danger,
        custom_id="buttonX",
    )
    async def button_x_callback(
        self,
        interaction_x: discord.Interaction,
        button_x: discord.ui.Button,
    ) -> None:
        self.x_id: int = interaction_x.user.id
        if self.x_id == self.o_id:
            await interaction_x.response.send_message(
                content="❌ You cannot impersonate others! 你不能冒充其他人！❌",
                ephemeral=True,
            )
            return
        await self.global_callback(interaction_x, button_x)

    async def on_timeout(self) -> None:
        self.clear_items()
        await self.cmd_interaction.delete_original_response()


if __name__ == "__main__":
    pass
