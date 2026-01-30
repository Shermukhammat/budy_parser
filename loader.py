import asyncio, os, sys
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from parser import parser_music

load_dotenv()

GROUP_USERNAME = os.getenv("GROUP_USERNAME")
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")
PHONE_NUM = os.getenv("PHONE_NUM")


queries = []
lock = asyncio.Lock()


async def add_query(query: str):
    if not query:
        return
    
    async with lock:
        queries.append(query)

async def pop_query() -> str:
    async with lock:
        if queries:
            return queries.pop()


clent = Client("sher", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUM)