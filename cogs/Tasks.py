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
    """
    Cog extension class for handling repeating tasks

    Args:
        bot (Bot): The Discord bot object
    
    Methods:
        cog_unload: Placeholder
        giveaway_announce: A task to draw giveaway winner(s) and announce them
        before_giveaway_announce: Start the task only after bot startup
        after_giveaway_announce: Placeholder
    """
    def __init__(self, bot):
        super().__init__(bot)
        self.giveaway_announce.start()


    def cog_unload(self):
        """Placeholder, not used"""
        self.giveaway_announce.cancel()


    # Giveaway winner announcement
    @tasks.loop(minutes=1)
    async def giveaway_announce(self) -> None:
        """Randomly draw and announce a giveaway's winner(s)
        
        1.  Retrieve the nearest ending giveaway from activity board and randomly draw
            winner(s) using GST.random_draw() function, returns a tuple containing an
            indicator, an index, a message ID, and winner(s) ID
        2.  The indicator is 0 or 1 where 0 = Inactive/ active but not ending giveaway,
            and 1 = active and ending giveaway. If indicator = 0 then end the task
            until next loop
        3.  If indicator = 1 then 1st) fetch the original Discord giveaway message in
            a specified channel using the message ID, 2nd) reply to the message
            stating the winner(s)
        4.  Update the original giveaway message with winner(s) and final entries,
            then remove the join_giveaway_button
        5.  Update the 'Winner(s)' cell in activity board with winner(s) ID

        Returns:
            None
        """
        # Draw the active giveaway winner(s)
        activity_sheet: pygsheets = GST.GSTSheet.wks1
        my_id: int = int(open('./credentials/my_id.txt').read())
        indicator, index, message_id, winners_id = GST.random_draw(
            sheet_df=activity_sheet.get_as_df(),
            now_time=round(functions.get_time().timestamp()),
        )

        if indicator == 0:
            return

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
            value=" & ".join(f"<@{winner[0]}>" for winner in winners_id),
            inline=False,
        )
        await message.edit(embed=embed, view=None)

        # Update the winners in the activity board sheet
        activity_sheet.update_value(
            addr=(index + 2, 4),
            val=", ".join(f"{winner[0]}" for winner in winners_id),
        )


    @giveaway_announce.before_loop
    async def before_giveaway_announce(self) -> None:
        """Only perform task after bot startup"""
        await self.bot.wait_until_ready()


    # Actions to perform AFTER giveaway winner announcement
    @giveaway_announce.after_loop
    async def after_giveaway_announce(self) -> None:
        """Placeholder, not used"""
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(Tasks(bot))


if __name__ == "__main__":
    pass
