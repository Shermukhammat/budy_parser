import asyncio, os, sys
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv


load_dotenv()

GROUP_USERNAME = os.getenv("GROUP_USERNAME")
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")
PHONE_NUM = os.getenv("PHONE_NUM")
SLEEPTIME = os.getenv("SLEEPTIME") or 30




CURENT_SEARCH_MESSAGE : Message  = None
MUSICS : list[Message] = []

lock = asyncio.Lock()
musics_lock = asyncio.Lock()

async def pop_audio() -> Message | None:
    async with musics_lock:
        if MUSICS:
            return MUSICS.pop(0)

async def add_audio(message: Message):
    async with musics_lock:
        MUSICS.append(message)

async def clean_audios():
    async with musics_lock:
        MUSICS.clear()


async def update_search_message(message: Message):
    global CURENT_SEARCH_MESSAGE
    async with lock:
        CURENT_SEARCH_MESSAGE = message 

async def delete_search_message():
    global CURENT_SEARCH_MESSAGE
    async with lock:
        CURENT_SEARCH_MESSAGE = None


async def get_search_message() -> Message | None:
    global CURENT_SEARCH_MESSAGE
    for _ in range(60):
        await asyncio.sleep(1)
        
        async with lock:
            if CURENT_SEARCH_MESSAGE:
                return CURENT_SEARCH_MESSAGE
    





clent = Client("sher", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUM)