from discord.ext import commands


## Universal bot import for other parts of the code
class Cog_Extension(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


if __name__ == "__main__":
    pass