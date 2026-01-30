import asyncio, os, sys
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv


load_dotenv()

GROUP_USERNAME = os.getenv("GROUP_USERNAME")
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")
PHONE_NUM = os.getenv("PHONE_NUM")


queries = []
audio_messages = []
queries_lock = asyncio.Lock()
audio_messages_lock = asyncio.Lock()



async def add_query(query: str):
    if not query:
        return
    
    async with queries_lock:
        queries.append(query)

async def pop_query() -> str:
    async with queries_lock:
        if queries:
            return queries.pop(0)

async def clear_queries():
    async with queries_lock:
        queries.clear()



async def add_audio(audio: Message):
    async with audio_messages_lock:
        audio_messages.append(audio)

async def pop_audio() -> Message:
    async with audio_messages_lock:
        if audio_messages:
            return audio_messages.pop(0)

async def clear_audio():
    async with audio_messages_lock:
        audio_messages.clear()




clent = Client("sher", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUM)