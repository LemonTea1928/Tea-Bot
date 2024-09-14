"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                        Wordle

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import random
from collections.abc import Generator

import discord


EMOJI_CODES = {
    "green": {
        "a": "<:green_a:1284445329910927421>",
        "b": "<:green_b:1284445351587090432>",
        "c": "<:green_c:1284445359094894746>",
        "d": "<:green_d:1284445366393241640>",
        "e": "<:green_e:1284445373263384640>",
        "f": "<:green_f:1284445384139214958>",
        "g": "<:green_g:1284445404091383808>",
        "h": "<:green_h:1284445415487569974>",
        "i": "<:green_i:1284445423439708163>",
        "j": "<:green_j:1284445433111777350>",
        "k": "<:green_k:1284445445132652586>",
        "l": "<:green_l:1284445457870884925>",
        "m": "<:green_m:1284445463587721330>",
        "n": "<:green_n:1284445470852124844>",
        "o": "<:green_o:1284445477663805532>",
        "p": "<:green_p:1284445484584538133>",
        "q": "<:green_q:1284445492230623253>",
        "r": "<:green_r:1284445499268665387>",
        "s": "<:green_s:1284445506298449944>",
        "t": "<:green_t:1284445513374236712>",
        "u": "<:green_u:1284445523004358697>",
        "v": "<:green_v:1284445530419761240>",
        "w": "<:green_w:1284445536849498153>",
        "x": "<:green_x:1284445543111725161>",
        "y": "<:green_y:1284445549558239283>",
        "z": "<:green_z:1284445556415922209>",
    },
    "yellow": {
        "a": "<:yellow_a:1284445594944798741>",
        "b": "<:yellow_b:1284445608312049757>",
        "c": "<:yellow_c:1284445630185476167>",
        "d": "<:yellow_d:1284445637785686026>",
        "e": "<:yellow_e:1284445644228132904>",
        "f": "<:yellow_f:1284445651202998356>",
        "g": "<:yellow_g:1284445657545052222>",
        "h": "<:yellow_h:1284445663303569418>",
        "i": "<:yellow_i:1284445669943414845>",
        "j": "<:yellow_j:1284445675618045963>",
        "k": "<:yellow_k:1284445682069147769>",
        "l": "<:yellow_l:1284445688276455486>",
        "m": "<:yellow_m:1284445695587258440>",
        "n": "<:yellow_n:1284445703321419816>",
        "o": "<:yellow_o:1284445709545767006>",
        "p": "<:yellow_p:1284445715640221777>",
        "q": "<:yellow_q:1284445721726156875>",
        "r": "<:yellow_r:1284445731108683776>",
        "s": "<:yellow_s:1284445738973138944>",
        "t": "<:yellow_t:1284445745289891892>",
        "u": "<:yellow_u:1284445751971156011>",
        "v": "<:yellow_v:1284445759013523486>",
        "w": "<:yellow_w:1284445765606838282>",
        "x": "<:yellow_x:1284445772275781723>",
        "y": "<:yellow_y:1284445778118447115>",
        "z": "<:yellow_z:1284445785714462822>",
    },
    "gray": {
        "a": "<:gray_a:1284445810104471594>",
        "b": "<:gray_b:1284445820552216629>",
        "c": "<:gray_c:1284445827343056936>",
        "d": "<:gray_d:1284445859605643295>",
        "e": "<:gray_e:1284445867251732536>",
        "f": "<:gray_f:1284445873899569225>",
        "g": "<:gray_g:1284445879557820477>",
        "h": "<:gray_h:1284445886742528114>",
        "i": "<:gray_i:1284445892270624768>",
        "j": "<:gray_j:1284445897861627915>",
        "k": "<:gray_k:1284445904681566268>",
        "l": "<:gray_l:1284445910113190010>",
        "m": "<:gray_m:1284445915079376936>",
        "n": "<:gray_n:1284445920511000616>",
        "o": "<:gray_o:1284445926290751581>",
        "p": "<:gray_p:1284445931902730252>",
        "q": "<:gray_q:1284445937346809957>",
        "r": "<:gray_r:1284445942585626686>",
        "s": "<:gray_s:1284445948449263676>",
        "t": "<:gray_t:1284445955160281111>",
        "u": "<:gray_u:1284445961468383355>",
        "v": "<:gray_v:1284445968267218954>",
        "w": "<:gray_w:1284445975100002387>",
        "x": "<:gray_x:1284445981894770719>",
        "y": "<:gray_y:1284445988030906379>",
        "z": "<:gray_z:1284445995530194954>",
    },
}


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
    
    if guessed_word == word:
        return list(zip([CORRECT_GREEN for _ in range(5)], [*guessed_word]))
    
    if len([1 for letter in guessed_word if letter not in word]) == 5:
        return list(zip([INCORRECT_GRAY for _ in range(5)], [*guessed_word]))
    
    word = list(word)
    encoded_letters: list = [(INCORRECT_GRAY, letter) for letter in guessed_word]
    for index, letter in enumerate(guessed_word):
        if letter == word[index]:
            encoded_letters[index] = (CORRECT_GREEN, letter)
            word[index] = None
    for index, letter in enumerate(guessed_word):
        if letter in word:
            encoded_letters[index] = (CHANGE_YELLOW, letter)
            word[word.index(letter)] = None
    
    return encoded_letters


def get_word_emojis(encoded_letters: list[tuple[str]]) -> str:
    codes = [EMOJI_CODES[colour][letter] for colour, letter in encoded_letters]
    return "".join(codes)


def emoji_to_msg(word: str, guessed_word: str) -> str:
    return get_word_emojis(check_word(word, str(guessed_word)))


class StartView(discord.ui.View):
    """
    A subclassed Button for starting Wordle.
    
    Attributes:
        cmd_interaction (discord.Interaction): From slash command
        word (str): A stripped and randomly-drawn word for guessing
    """
    def __init__(self, cmd_interaction: discord.Interaction) -> None:
        self.cmd_interaction: discord.Interaction = cmd_interaction
        self.canvas: list[str] = ["◻️" * 5 for _ in range(6)]
        self.word: str = next(read_one_word()).strip()
        super().__init__(timeout=None)
    
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
            content="\n".join(self.canvas),
            view=GameView(self.cmd_interaction, self.word, self.canvas),
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
        self,
        cmd_interaction: discord.Interaction,
        word: str,
        canvas: str,
        guess: int = 0,
    ) -> None:
        self.cmd_interaction: discord.Interaction = cmd_interaction
        self.word: str = word
        self.canvas: str = canvas
        self.guess: int = guess
        self.abandon_button_clicked: bool = False
        super().__init__(timeout=None)
    
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
        await interaction.response.send_modal(
            GUI(self.cmd_interaction, self.word, self.canvas, self.guess)
        )
    
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
    
    def __init__(
        self,
        cmd_interaction: discord.Interaction,
        word: str,
        canvas: str,
        guess: int,
    ) -> None:
        self.cmd_interaction: discord.Interaction = cmd_interaction
        self.word: str = word
        self.canvas: str = canvas
        self.guess: int = guess
        super().__init__(timeout=None)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if not is_valid(self.guessed_word.value):
            await interaction.response.send_message(
                content="❌ Invalid word! 無效字詞！\n"
                "(This message deletes in 3s... 此訊息將在3秒內刪除...)",
                delete_after=3.0,
                ephemeral=True,
            )
            return
        
        self.guess += 1
        self.canvas[self.guess - 1] = emoji_to_msg(
            self.word,
            self.guessed_word.value,
        )

        if self.guessed_word.value == self.word:
            await interaction.response.edit_message(
                content="\n".join(self.canvas),
                embed=discord.Embed(title="🥳 You guessed it! 你猜到了！"),
                view=None,
            )
            return
        
        if (self.guessed_word.value != self.word) and (self.guess == 6):
            await interaction.response.edit_message(
                content="\n".join(self.canvas),
                embed=discord.Embed(
                    title=f"🔊 Game over! 遊戲結束！\nAnswer is {self.word}"
                ),
                view=None,
            )
            return
        
        view = GameView(
            self.cmd_interaction,
            self.word,
            self.canvas,
            self.guess,
        )
        
        await interaction.response.edit_message(
            content="\n".join(self.canvas),
            view=view,
        )


if __name__ == '__main__':
    pass
