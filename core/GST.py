"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                Giveaway Setup Tool (GST)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import core.functions as functions

import time
import datetime

import discord
import pygsheets
import pandas as pd
import numpy as np


"""
Giveaway end time calculator
"""


def get_end_time(
    now_time: datetime.datetime,
    time: discord.ui.TextInput,
) -> int:
    time2float: float = float(time.value)
    end_time: datetime.datetime = now_time + datetime.timedelta(days=time2float)
    del time2float
    return round(end_time.timestamp())


"""
Giveaway embed creator
"""


def createEmbed(name, prize, num, time) -> tuple[discord.Embed, int]:
    now_time: datetime.datetime = functions.get_time()
    end_time: int = get_end_time(now_time=now_time, time=time)

    embed: discord.Embed = discord.Embed(
        title=f"{name}",
        description=f"{prize}",
        timestamp=now_time,
        color=discord.Color.from_str("#e2ab55"),
    )
    embed.set_thumbnail(
        url=(
            "https://static.wikia.nocookie.net/warframe/images/e/e7/"
            "PlatinumLarge.png/revision/latest?cb=20130728181159"
        ),
    )
    embed.add_field(
        name="End time 結束時間: ",
        value=f"<t:{end_time}:f>",
        inline=False,
    )
    embed.add_field(
        name="Winner(s) 得獎者",
        value=num,
        inline=False,
    )
    embed.add_field(
        name="Entries 參加人數",
        value=0,
        inline=False,
    )
    del now_time
    return embed, end_time


"""
Giveaway entries checker
"""


def checker(
    current_sht: pygsheets.Worksheet,
    embed: discord.Embed,
) -> discord.Embed:
    id_list: np.ndarray = np.array(current_sht.get_all_values())
    embed.set_field_at(
        index=2,
        name="Entries 參加人數",
        value=id_list.shape[0] - 1,
    )
    del id_list
    return embed


"""
Giveaway random drawer
"""


def random_draw(
    sheet_df: pd.DataFrame,
    now_time: int,
) -> tuple[int, int, int, np.ndarray]:
    activity: pd.DataFrame = sheet_df.drop(
        labels=["Giveaway name", "Giveaway prize"],
        axis=1,
    )
    activity: pd.DataFrame = activity[
        (activity["1 (Active) | 0 (Inactive)"] == 1)
        & (activity["Ending time"] <= now_time)
    ]
    for row in activity.itertuples():
        index, message_id, num_winners = row[0], row[1], row[2]
        # Go to the corresponding giveaway worksheet
        sheet: pygsheets = GSTSheet.sht.worksheet_by_title(
            title=f"{message_id}",
        )
        # Only extract user ID & winner(s) using sample() function
        sheet_df: pd.DataFrame = sheet.get_as_df().select_dtypes(
            include=["integer"],
        )
        winners_id: np.ndarray = sheet_df.sample(n=num_winners).values
        # Assign the giveaway as 0 (inactive)
        sheet: pygsheets = GSTSheet.wks1
        sheet.update_value(addr=(index + 2, 6), val=0)

        del activity, sheet, sheet_df, num_winners
        return 1, index, message_id, winners_id
    del activity
    return 0, 0, 0, np.array([0])


"""
Active giveaway end time retriever (formatted as datetime.time)
"""


def end_time_retrieve(sheet_df: pd.DataFrame) -> list:
    time_zone: datetime.timezone = datetime.timezone(
        offset=datetime.timedelta(hours=8),
        name="utc",
    )
    sheet_df: pd.DataFrame = sheet_df.select_dtypes(
        include=["integer"],
    )
    sheet_df: pd.DataFrame = sheet_df[sheet_df["1 (Active) | 0 (Inactive)"] == 1]
    end_time_list = [
        datetime.datetime.fromtimestamp(day, time_zone).time()
        for day in sheet_df["Ending time"].tolist()
    ]
    del time_zone, sheet_df
    return end_time_list


"""
GST GUI
"""


class GUI(discord.ui.Modal, title="🎁 Giveaway Setup Tool (GST)"):
    name: discord.ui.TextInput = discord.ui.TextInput(
        label="Name 名稱",
        min_length=1,
        max_length=50,
    )
    prize: discord.ui.TextInput = discord.ui.TextInput(
        label="Prize description 獎品描述",
        min_length=1,
        max_length=100,
        style=discord.TextStyle.paragraph,
    )
    num: discord.ui.TextInput = discord.ui.TextInput(
        label="Number of winner(s) 得獎人數",
        min_length=1,
        max_length=50,
    )
    time: discord.ui.TextInput = discord.ui.TextInput(
        label="Duration (in days) 時長（日）",
        min_length=1,
        max_length=50,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        embed, end_time = createEmbed(
            self.name,
            self.prize,
            self.num,
            self.time,
        )
        view = GSTButtonView()
        sheet = GSTSheet()
        await interaction.response.send_message(
            embed=embed,
            view=view,
        )
        message: discord.InteractionMessage = await interaction.original_response()
        setattr(sheet, "message", message)
        setattr(sheet, "name", self.name)
        setattr(sheet, "prize", self.prize)
        setattr(sheet, "num", self.num)
        setattr(sheet, "end_time", end_time)
        sheet.sheet_initialize()

        del end_time, embed, view, sheet, message


"""
GST button under embed
"""


class GSTButtonView(discord.ui.View):
    def __init__(self) -> None:
        self.wks: pygsheets = GSTSheet.wks
        super().__init__(timeout=None)

    @discord.ui.button(
        style=discord.ButtonStyle.green, custom_id="join_giveaway_button", emoji="👈"
    )
    async def on_button_click(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        # Retrieve the user's name & ID, and message ID on click and put them on the sheet
        user: discord.User = interaction.user
        values: list[str, str] = [[user.name, f"{user.id}"]]
        message: discord.Message = interaction.message
        embed: discord.Embed = message.embeds[0]
        # Check if the sheet with corresponding message exists
        try:
            current_sht: pygsheets = GSTSheet.sht.worksheet_by_title(
                title=f"{message.id}",
            )
            current_sht_array: np.ndarray = np.array(
                current_sht.get_col(col=2),
            )
            # Check if the user has joined the corresponding giveaway
            if f"{user.id}" in current_sht_array:
                await interaction.response.send_message(
                    content="❗ You've already joined! 你已經參加了！",
                    ephemeral=True,
                )
                await message.edit(embed=checker(current_sht, embed))
                time.sleep(0.5)
                del (user, values, message, embed, current_sht, current_sht_array)
                return
            # Add the user to the sheet database for the giveaway random draw
            try:
                current_sht.append_table(values=values)
            except Exception:
                await interaction.response.send_message(
                    content="✅ Successfully joined! 成功參加！",
                    ephemeral=True,
                )
                await message.edit(embed=checker(current_sht, embed))
                del (user, values, message, embed, current_sht, current_sht_array)

        except Exception:
            await interaction.response.send_message(
                content="❌ This giveaway does not exist or has ended! "
                "這個抽獎活動不存在或已結束！",
                ephemeral=True,
            )
            del user, values, message, embed


"""
GST google sheet database
"""


class GSTSheet:
    # Load the worksheet as a new tab for storage
    url: str = open('core/url.txt', 'r').readline()
    gc: pygsheets = pygsheets.authorize(
        service_account_file="cogs/GSTcredentials.json"
    )
    sht: pygsheets = gc.open_by_url(url)
    wks: pygsheets = sht.worksheet_by_title("Template")
    wks1: pygsheets = sht.worksheet_by_title("Activity board")

    def sheet_initialize(self) -> None:
        # Copy the worksheet as a new tab
        values = [
            [
                str(self.message.id),
                str(self.name),
                str(self.prize),
                str(self.num),
                str(self.end_time),
                1,
            ]
        ]
        self.sht.add_worksheet(
            title=values[0][0],
            src_worksheet=self.wks,
        )
        try:
            self.wks1.append_table(values=values)
        except Exception:
            pass

        del values


if __name__ == "__main__":
    pass
