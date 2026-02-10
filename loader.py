import asyncio, os, sys
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv


load_dotenv()

GROUP_USERNAME = os.getenv("GROUP_USERNAME")
API_HASH = os.getenv("API_HASH")
PHONE_NUM = os.getenv("PHONE_NUM")

def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default

API_ID = _env_int("API_ID", 0)
SLEEPTIME = _env_int("SLEEPTIME", 30)
PAGE_COUNT = _env_int("PAGE_COUNT", 2)




CURENT_SEARCH_MESSAGE : Message  = None
MUSICS : list[Message] = []

lock = asyncio.Lock()
musics_lock = asyncio.Lock()

async def pop_audio(wait_time: int = 60) -> Message | None:
    for _ in range(wait_time):
        async with musics_lock:
            if MUSICS:
                return MUSICS.pop(0)
        await asyncio.sleep(1)

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


async def get_search_message(wait: int = 60) -> Message | None:
    global CURENT_SEARCH_MESSAGE
    for _ in range(wait):
        await asyncio.sleep(1)
        
        async with lock:
            if CURENT_SEARCH_MESSAGE:
                return CURENT_SEARCH_MESSAGE
    





clent = Client("sher", api_id=API_ID or None, api_hash=API_HASH, phone_number=PHONE_NUM)
