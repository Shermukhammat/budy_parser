from dotenv import load_dotenv
from pyrogram import Client 
from pyrogram.types import Message
from loader import pop_audio, clean_audios, get_search_message, delete_search_message, SLEEPTIME, PAGE_COUNT
import os, asyncio
from pathvalidate import sanitize_filename
from pathlib import Path
from dotenv import load_dotenv 


if not os.path.exists("files"):
    os.mkdir("files")

load_dotenv()
SAVE_PATH = Path(os.getenv("SAVE_PATH", "D:/fleshka"))

async def parser_music(query: str, clent: Client):
    await clean_audios()
    await delete_search_message()    
    await clent.send_message("@Music_to_you_bot", query)

    folder_name = sanitize_filename(query, platform="windows")
    save_folder = SAVE_PATH / folder_name
    save_folder.mkdir(parents=True, exist_ok=True)

    msg = await get_search_message()
    if not msg:
        return
    
    for page in range(1, PAGE_COUNT+1):
        await parse_from_inline(msg, clent, save_folder)
        if page == PAGE_COUNT:
            break
        
        await delete_search_message()
        await press_next_button(clent, msg)
        msg = await get_search_message()
        if not msg:
            break


async def parse_from_inline(msg: Message, clent: Client, save_folder: Path):
    if not msg.reply_markup or len(msg.reply_markup.inline_keyboard) != 12:
        return
            
    await asyncio.sleep(2)
    for row in msg.reply_markup.inline_keyboard[1:11]:
        print(row[0].text)
        await clent.request_callback_answer("@Music_to_you_bot", msg.id, row[0].callback_data)
        await asyncio.sleep(5)
        audio_msg = await pop_audio()
        await download_music(audio_msg, save_folder)

async def press_next_button(clent: Client, msg: Message) -> bool:
    if not msg.reply_markup or len(msg.reply_markup.inline_keyboard) != 12:
        return False
    
    if "➡️" in msg.reply_markup.inline_keyboard[-1][-1].text:
        await asyncio.sleep(2)
        callback_data = msg.reply_markup.inline_keyboard[-1][-1].callback_data
        await clent.request_callback_answer("@Music_to_you_bot", msg.id, callback_data)
   
    return True

async def download_music(audio_msg: Message, save_floder: str):
    if audio_msg:
        file_path = f"{save_floder}/{audio_msg.audio.file_name}"
        if os.path.exists(file_path):
            await asyncio.sleep(3)
            return
        
        await audio_msg.download(file_path)
        await asyncio.sleep(SLEEPTIME)