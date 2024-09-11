from discord.ext import commands


class Cog_Extension(commands.Cog):
    """Bot object to be passed to other modules"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


if __name__ == "__main__":
    pass