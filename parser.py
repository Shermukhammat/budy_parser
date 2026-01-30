from dotenv import load_dotenv
from pyrogram import Client 
from pyrogram.types import Message
from loader import GROUP_USERNAME, pop_audio
import os, asyncio


if not os.path.exists("files"):
    os.mkdir("files")



async def parser_music(query: str, clent: Client):
    query_msg = await clent.send_message("@Music_to_you_bot", query)

    async for msg in clent.get_chat_history("@Music_to_you_bot", limit=5, offset_id=query_msg.id):

        if isinstance(msg, Message) and msg.caption and msg.caption.startswith("🎧") and not msg.audio:
            if len(msg.reply_markup.inline_keyboard) != 12:
                return
            
            for row in msg.reply_markup.inline_keyboard[1:11]:
                print(row[0].text)
                await clent.request_callback_answer("@Music_to_you_bot", msg.id, row[0].callback_data)
                await asyncio.sleep(5)
                audio_msg = await pop_audio()
                if audio_msg:
                    pass


async def download_music():
    pass