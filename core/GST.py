"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

                                Giveaway Setup Tool (GST)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import pygsheets.client
import core.functions as functions

import time
import datetime

import discord
import pygsheets
import pandas as pd
import numpy as np


def get_end_time(now_time: datetime.datetime, time: discord.ui.TextInput) -> int:
    """
    Calculate a giveaway's end time
    
    Args:
        now_time (datetime): Current time
        time (TextInput -> str): GUI input for giveaway duration (in days)
    
    Returns:
        round(end_time.timestamp()) (int): Rounded float timestamp
    """
    end_time: datetime.datetime = now_time + datetime.timedelta(days=float(time.value))
    return round(end_time.timestamp())


def createEmbed(name, prize, num, time) -> tuple[discord.Embed, int]:
    """
    Create a giveaway embed upon submission of the GUI
    
    Args:
        name (TextInput -> str): Name of the giveaway
        prize (TextInput -> str): Prize of the giveaway
        num (TextInput -> int): Number of winner(s) of the giveaway
        time (TextInput -> float): Duration of the giveaway (in days)
    
    Returns:
        embed (Embed): The completed giveaway info embed
        end_time (int): 
    """
    now_time: datetime.datetime = functions.get_time()
    end_time: int = get_end_time(now_time=now_time, time=time)
    
    embed: discord.Embed = discord.Embed(
        title=f"{name}",
        description=f"{prize}",
        timestamp=now_time,
        color=discord.Color.from_str("#ffa500"),
    )
    embed.set_thumbnail(url=open('./credentials/plat_url.txt').read())
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


def checker(current_sht: pygsheets.Worksheet, embed: discord.Embed) -> discord.Embed:
    """
    Check the number of entries in a giveaway
    
    1.  Retrieve all cells in a particular giveaway worksheet as an array
    2.  Update the number of its rows (id_array.shape[0]) to embed's "Entries"
    
    Args:
        current_sht (Worksheet): Worksheet with the giveaway message ID as title
        embed (Embed): The corresponding giveaway embed
    
    Returns:
        embed (Embed): The embed with updated number of entries
    """
    id_array: np.ndarray = np.array(current_sht.get_all_values())
    embed.set_field_at(
        index=2,
        name="Entries 參加人數",
        value=id_array.shape[0] - 1,
    )
    del id_array
    return embed


def random_draw(
    sheet_df: pd.DataFrame, now_time: int
) -> tuple[int, int, int, np.ndarray]:
    """
    Randomly draw winner(s) from a giveaway
    
    1.  Extract the activity board as a DataFrame, filter out text columns and
        giveaways that are active and ending
    2.  If the DataFrame is empty then return a tuple with indicator = 0
    3.  If not empty then draw winner(s) and return a tuple with indicator = 1
    
    Args:
        sheet_df (DataFrame): The activity board worksheet in DataFrame format
    
    Returns:
        If active giveaway & has ended: (1, index, message_id, winners_id) 
        If inactive/ (active & has ended) giveaway: (0, 0, 0, np.array[0])
    """
    activity: pd.DataFrame = sheet_df.drop(
        labels=["Giveaway name", "Giveaway prize"],
        axis=1,
    )
    activity: pd.DataFrame = activity[
        (activity["1 (Active) | 0 (Inactive)"] == 1)
        & (activity["Ending time"] <= now_time)
    ]
    
    if activity.empty:
        return 0, 0, 0, np.array([0])
    
    for row in activity.itertuples():
        index, message_id, num_winners = row[0], row[1], row[2]
        
        sheet: pygsheets = GSTSheet.sht.worksheet_by_title(title=f"{message_id}")
        sheet_df: pd.DataFrame = sheet.get_as_df().select_dtypes(include=["integer"])
        winners_id: np.ndarray = sheet_df.sample(n=num_winners).to_numpy()
        
        GSTSheet.wks1.update_value(addr=(index + 2, 6), val=0,)
        
        return 1, index, message_id, winners_id


def end_time_retrieve(sheet_df: pd.DataFrame) -> list:
    """
    Retrieve active giveaway end_time (formatted as datetime.time)
    
    Args:
        sheet_df (DataFrame): The activity board worksheet in DataFrame format
    
    Returns:
        end_time_list (list): A list containing all active giveaway end time
    """
    time_zone = datetime.timezone(
        offset=datetime.timedelta(hours=8), 
        name="utc",
    )
    
    sheet_df: pd.DataFrame = sheet_df.select_dtypes(include=["integer"])
    sheet_df: pd.DataFrame = sheet_df[sheet_df["1 (Active) | 0 (Inactive)"] == 1]
    end_time_list = [
        datetime.datetime.fromtimestamp(day, time_zone).time()
        for day in sheet_df["Ending time"].tolist()
    ]
    
    return end_time_list


class GUI(discord.ui.Modal, title="🎁 Giveaway Setup Tool (GST)"):
    """
    Interactive GUI subclass for easy giveaway setup
    
    Attributes:
        name (discord.ui.TextInput -> str): Name of the giveaway
        prize (discord.ui.TextInput -> str): Prize for the giveaway
        num (discord.ui.TextInput -> int): Number of winner(s) of the giveaway
        time (discord.ui.TextInput -> float): Duration of the giveaway in day(s)
    """
    name = discord.ui.TextInput(
        label="Name 名稱",
        min_length=1,
        max_length=50,
    )
    prize = discord.ui.TextInput(
        label="Prize description 獎品描述",
        min_length=1,
        max_length=100,
        style=discord.TextStyle.paragraph,
    )
    num = discord.ui.TextInput(
        label="Number of winner(s) 得獎人數",
        min_length=1,
        max_length=50,
    )
    time = discord.ui.TextInput(
        label="Duration (in days) 時長（日）",
        min_length=1,
        max_length=50,
    )
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Built-in discord.py method for GUI submit detection, on submit:
        
        1.  Create an embed containing the giveaway info
        2.  Create a view object containing a button to join the giveaway
        3.  Create a Google Sheet (worksheet) object as a database
        4.  Send a Discord message containing the embed & view
        
        Args:
            interaction: The action when the user presses 'Submit' button
        
        Returns:
            None
        """
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
        
        message = await interaction.original_response()
        setattr(sheet, "message", message)
        setattr(sheet, "name", self.name)
        setattr(sheet, "prize", self.prize)
        setattr(sheet, "num", self.num)
        setattr(sheet, "end_time", end_time)
        sheet.sheet_initialize()
        
        del end_time, embed, view, sheet, message


class GSTButtonView(discord.ui.View):
    """
    A discord.ui.View subclass containing a button to join the giveaway
    
    Args:
        wks (pygsheets): The Google Sheet database template for copying
        timeout: None
    """
    def __init__(self) -> None:
        self.wks: pygsheets = GSTSheet.wks
        super().__init__(timeout=None)
    
    @discord.ui.button(
        style=discord.ButtonStyle.green,
        custom_id="join_giveaway_button",
        emoji="👈",
    )
    async def on_button_click(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ) -> None:
        """Built-in discord.py method for button callback on click, on click:
        
        1.  Retrieve user name & ID, giveaway message, and the message embed
        2.  Try locating the worksheet linking to the giveaway, if none is found
            then send a message warning it doesn't exist or has ended
        3.  If the giveaway is found then check if the user who click the button
            has joined it already, otherwise warn the user they have joined
        4.  If the user hasn't joined the giveaway then add their ID to database
            and prompt them they have successfully joined
        
        (In 3 & 4 whenever a user clicks the button, the embed will be updated
        with the latest number of entries from the database)
        
        Args:
            interaction: The action when the user presses 'join_giveaway_button'
            button: The 'join_giveaway_button'
        
        Returns:
            None
        """
        user: discord.User = interaction.user
        values: list[list[str]] = [[user.name, f"{user.id}"]]
        message: discord.Message = interaction.message
        embed: discord.Embed = message.embeds[0]
        
        try:
            current_sht: pygsheets = GSTSheet.sht.worksheet_by_title(
                title=f"{message.id}",
            )
            current_sht_array: np.ndarray = np.array(
                current_sht.get_col(col=2),
            )
        except Exception:
            await interaction.response.send_message(
                content="❌ This giveaway does not exist or has ended! "
                "這個抽獎活動不存在或已結束！",
                ephemeral=True,
            )
            return
        
        if f"{user.id}" in current_sht_array:
            await interaction.response.send_message(
                content="❗ You've already joined! 你已經參加了！",
                ephemeral=True,
            )
            await message.edit(embed=checker(current_sht, embed))
            return
        
        try:
            current_sht.append_table(values=values)
        except Exception:
            await interaction.response.send_message(
                content="✅ Successfully joined! 成功參加！",
                ephemeral=True,
            )
            await message.edit(embed=checker(current_sht, embed))
            return


class GSTSheet:
    """
    Google Sheet database class for individual tracking of giveaways
    
    Attributes:
        url (str): The spreadsheet file URL on Google Drive
        gc (pygsheets.client): Google Sheet API client
        sht (pygsheets): The spreadsheet database
        wks (pygsheets): The 'Template' worksheet inside sht for duplication
        wks1 (pygsheets): The 'Activity board' worksheet tracking each giveaway status
    
    Methods:
        sheet_initialize: Initialize a new giveaway worksheet upon submission of GUI
    """
    url: str = open('./credentials/sheet_url.txt').read()
    gc: pygsheets.client = pygsheets.authorize(
        service_account_file='./credentials/GSTcredentials.json',
    )
    sht: pygsheets = gc.open_by_url(url)
    wks: pygsheets = sht.worksheet_by_title("Template")
    wks1: pygsheets = sht.worksheet_by_title("Activity board")
    
    def sheet_initialize(self) -> None:
        """
        Method for creating a new worksheet when a giveaway is created from GUI
        
        1.  Create a nested list (representative of a spreadsheet cell) containing
            all the giveaway information; the integer 1 means the giveaway is active
        2.  Add a new worksheet with the giveaway message ID as title, by copying
            the template worksheet
        3.  Add the nested list to the last row of the activity board
        
        Returns:
            None
        """
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
        self.sht.add_worksheet(title=values[0][0], src_worksheet=self.wks)
        self.wks1.append_table(values=values)
        
        del values


if __name__ == "__main__":
    pass
