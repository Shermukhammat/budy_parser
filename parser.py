from dotenv import load_dotenv
from pyrogram import Client 
import os 


load_dotenv()
GROUP_USERNAME = os.getenv("GROUP_USERNAME")


async def parser_music(query: str, clent: Client):
    query_msg = await clent.send_message("@Music_to_you_bot", query)

    print(query_msg.reply_markup)