"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                        Wordle

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import random
from collections.abc import Generator

import discord


global FALSE_GRAY; FALSE_GRAY: str = "gray"
global CORRECT_GREEN; CORRECT_GREEN: str = "green"
global CHANGE_YELLOW; CHANGE_YELLOW: str = "yellow"


def read_one_word() -> Generator[str, None, None]:
    """
    Open the 'popular words' dictionary text file and return a generator
    containing a randomly chosen 5-letter word
    
    Returns:
        Generator (str): Generator yielding a randomly chosen 5-letter word
    """
    with open("./miscellaneous/wordle_words.txt") as words:
        yield random.choice(words.readlines())


def get_word_emoji(colour: str, character: str) -> Generator[str, None, None]:
    with open("./miscellaneous/wordle_emojis.py") as emojis:
        yield 


def check_word():
    return


class StartView(discord.ui.View):
    """
    A subclassed Button for starting Wordle.
    
    Attributes:
        cmd_interaction (discord.Interaction): From slash command
        word (str): A randomly-drawn word for guessing
    """
    def __init__(self, cmd_interaction: discord.Interaction) -> None:
        self.cmd_interaction: discord.Interaction = cmd_interaction
        self.word: str = next(read_one_word())
        super().__init__()
    
    @discord.ui.button(
        label="Start 開始",
        style=discord.ButtonStyle.blurple,
        custom_id="start_wordle_button",
    )
    async def callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        """
        Built-in discord.py method for button callback. On click, add a blank
        Wordle canvas and two buttons (guess & abandon) to edit the message
        """
        await interaction.response.edit_message(
            content=f"{"◻️" * 5}\n" * 6,
            view=GameView(self.cmd_interaction, self.word),
        )


class GameView(discord.ui.View):
    """
    Subclassed Buttons for handling word-guessing and session-abandoning tasks

    Attributes:
        cmd_interaction (discord.Interaction): From slash command
        abandon_button_clicked (bool): Check if the abandon_button was clicked
        word (str): A randomly-drawn word for guessing
    """
    def __init__(
        self, cmd_interaction: discord.Interaction, word: str
    ) -> None:
        self.cmd_interaction: discord.Interaction = cmd_interaction
        self.abandon_button_clicked: bool = False
        self.word: str = word
        super().__init__()
    
    @discord.ui.button(
        label="😏 Guess 猜一下",
        style=discord.ButtonStyle.success,
        custom_id="guess_button",
    )
    async def guess_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        """
        Built-in discord.py method for button callback. On click, send a GUI
        prompting the user to type in a 5-letter word guess

        Args:
            word (str): The randomly-drawn word to be checked in GUI section
        """
        await interaction.response.send_modal(GUI(self.word))
    
    @discord.ui.button(
        label="😐 Abandon 放棄",
        style=discord.ButtonStyle.danger,
        custom_id="abandon_button",
    )
    async def abandon_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        """
        Built-in discord.py method for button callback. On click, first edit
        the button to confirm whether the user wants to abandon the session,
        if clicked again then the ephemeral message will be deleted

        Args:
            word (str): The randomly-drawn word to be checked in GUI section
        """
        if self.abandon_button_clicked:
            await self.cmd_interaction.delete_original_response()
            
        button.label = "❓ Confirm 確定"
        self.abandon_button_clicked = True
        await interaction.response.edit_message(view=self)


class GUI(discord.ui.Modal, title="😤 Guess it! 猜吧！"):
    """
    Interactive GUI subclass for typing in a guessed word
    
    Attributes:
        guess_word (discord.ui.TextInput -> str): The user-gussed word
        word (str): The randomly-drawn word to be checked here
    """
    guessed_word = discord.ui.TextInput(
        label="Required 必填",
        placeholder="Input a 5-letter word 鍵入一個五字詞",
        min_length=5,
        max_length=5,
    )
    
    def __init__(self, word: str) -> None:
        self.word: str = word
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            
        )


if __name__ == '__main__':
    pass
