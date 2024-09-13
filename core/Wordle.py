"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                        Wordle

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import random
from collections.abc import Generator

import discord


def read_one_word() -> Generator[str, None, None]:
    """
    Open the 'popular words' text file and randomly draw a word
    
    Returns:
        Generator (str): Generator yielding a randomly chosen 5-letter word
    """
    with open("./miscellaneous/wordle_words.txt") as words:
        yield random.choice(words.readlines())


def is_valid(guessed_word: str) -> bool:
    """
    Validate if the guessed word is valid

    Args:
        guessed_word (str): The user-guessed word for checking

    Returns:
        bool: Whether the word exists or not
    """
    with open("./miscellaneous/wordle_all_words.txt") as all_words:
        words = all_words.readlines()
    
    for word in words:
        if guessed_word in word: return True
    
    return False


def check_word(word :str, guessed_word: str) -> list[tuple[str]]:
    """
    Check if the guessed word is a correct answer, encode a specific colour
    for each letter in it where green is correct letter and position; yellow
    is correct word but incorrect position; gray is incorrect letter and
    position
    
    Args:
        word (str): The randomly-chosen word as the answer
        guessed_word (str): The user-guessed word for checking
    
    Returns:
        list: A list having 5 tuples, each encoding a colour for a letter
    """
    CORRECT_GREEN: str = "green"
    CHANGE_YELLOW: str = "yellow"
    INCORRECT_GRAY: str = "gray"
    
    if word is guessed_word:
        return list(zip([CORRECT_GREEN for _ in range(5)], [*word]))
    
    if len([1 for letter in guessed_word if letter not in word]) == 5:
        return list(zip([INCORRECT_GRAY for _ in range(5)], [*word]))
    
    encoded_letters: list = []
    for index, letter in enumerate(guessed_word):
        if letter not in word:
            encoded_letters.append((INCORRECT_GRAY, letter))
            continue
        elif letter is not word[index]:
            encoded_letters.append((CHANGE_YELLOW, letter))
            continue
        elif letter is word[index]:
            encoded_letters.append((CORRECT_GREEN, letter))
            continue
    
    return encoded_letters


def get_word_emoji(colour: str, character: str) -> Generator[str, None, None]:
    with open("./miscellaneous/wordle_emojis.py") as emojis:
        yield 


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
            content=f"{"◻️" * 5}\n" * 6 + self.word,
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
        if not is_valid(str(self.guessed_word)):
            await interaction.response.send_message(
                content="❌ Invalid word! 無效字詞！",
                delete_after=5.0,
                ephemeral=True,
            )
            return
        
        await interaction.response.edit_message(

        )


if __name__ == '__main__':
    pass
