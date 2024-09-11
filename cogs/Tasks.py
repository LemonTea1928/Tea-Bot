"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                    Cog - Tasks extension

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import core.GST as GST
import core.functions as functions
import core.classes as classes

import pandas as pd
import pygsheets
import discord
from discord.ext import commands, tasks


class Tasks(classes.Cog_Extension):
    def __init__(self, bot):
        super().__init__(bot)
        self.giveaway_announce.start()

    def cog_unload(self):
        self.giveaway_announce.cancel()

    # Giveaway winner announcement
    @tasks.loop(minutes=1)
    async def giveaway_announce(self) -> None:
        # Draw the active giveaway winner(s)
        activity_sheet: pygsheets = GST.GSTSheet.wks1
        sheet_df: pd.DataFrame = activity_sheet.get_as_df()
        now_time: int = round(functions.get_time().timestamp())
        my_id: int = int(open('./credentials/my_id.txt').read())

        indicator, index, message_id, winners_id = GST.random_draw(sheet_df, now_time)

        match indicator:
            case 0:
                return
            case 1:
                # Reply to the giveaway embed message
                channel: discord.GuildChannel = self.bot.get_channel(
                    int(open('./credentials/channel_id.txt').read()),
                )
                message: discord.Message = await channel.fetch_message(
                    message_id,
                )
                await message.reply(
                    "🥳 Congratulations to "
                    + ", ".join(f"<@{winner[0]}>" for winner in winners_id)
                    + " on winning this giveaway!\n"
                    f"<@{my_id}>"
                    " will contact you shortly afterwards.\n\n"
                    "🥳 恭喜 "
                    + ", ".join(f"<@{winner[0]}>" for winner in winners_id)
                    + " 贏得是次抽獎！\n"
                    f"<@{my_id}> 會在稍後時間聯絡你。"
                )

                # Update the giveaway embed message with final entries and winners
                current_sht: pygsheets = GST.GSTSheet.sht.worksheet_by_title(
                    title=f"{message_id}",
                )
                embed: discord.Embed = GST.checker(
                    current_sht=current_sht,
                    embed=message.embeds[0],
                )
                embed.set_field_at(
                    index=1,
                    name="Winner(s) 得獎者",
                    value="&".join(f"<@{winner[0]}>" for winner in winners_id),
                    inline=False,
                )
                await message.edit(embed=embed, view=None)

                # Update the winners in the activity board sheet
                activity_sheet.update_value(
                    addr=(index + 2, 4),
                    val=", ".join(f"{winner[0]}" for winner in winners_id),
                )
                print("Giveaway draw successfully ended.\n")

                del channel, message, current_sht, embed
        
        del activity_sheet, sheet_df, indicator, index, message_id, winners_id, my_id

    # Actions to perform BEFORE giveaway winner announcement
    @giveaway_announce.before_loop
    async def before_giveaway_announce(self) -> None:
        # Wait until the bot is online & ready
        await self.bot.wait_until_ready()

    # Actions to perform AFTER giveaway winner announcement
    @giveaway_announce.after_loop
    async def after_giveaway_announce(self) -> None:
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Tasks(bot))


# -------------------------------------End of code-------------------------------------


if __name__ == "__main__":
    pass
