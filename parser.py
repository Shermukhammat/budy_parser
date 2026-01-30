from dotenv import load_dotenv
from pyrogram import Client 
from pyrogram.types import Message
from loader import pop_audio, clean_audios, get_search_message, delete_search_message, SLEEPTIME
import os, asyncio
from pathvalidate import sanitize_filename


if not os.path.exists("files"):
    os.mkdir("files")



async def parser_music(query: str, clent: Client):
    await clean_audios()
    await delete_search_message()
    
    query_msg = await clent.send_message("@Music_to_you_bot", query)
    await asyncio.sleep(5)

    save_floder = f"files/{sanitize_filename(query)}"
    if not os.path.exists(save_floder):
        os.mkdir(save_floder)

    msg = await get_search_message()
    if not msg:
        return
    
    if not msg.reply_markup or len(msg.reply_markup.inline_keyboard) != 12:
        return
            
    await asyncio.sleep(2)
    for row in msg.reply_markup.inline_keyboard[1:11]:
        print(row[0].text)
        await clent.request_callback_answer("@Music_to_you_bot", msg.id, row[0].callback_data)
        await asyncio.sleep(5)
        audio_msg = await pop_audio()
        await download_music(audio_msg, save_floder)

async def download_music(audio_msg: Message, save_floder: str):
    if audio_msg:
        file_path = f"{save_floder}/{audio_msg.audio.file_name}"
        if os.path.exists(file_path):
            return
        
        await audio_msg.download(file_path)
        await asyncio.sleep(SLEEPTIME)