import asyncio, os, sys
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from loader import clent, add_query, pop_query
from parser import parser_music



@clent.on_message((filters.group) & (filters.text))
async def message_handler(client: Client, message: Message):
    global queries
    if message.text.startswith("/list"):
        await message.reply("\n".join(queries) or "List bo'sh")

    elif message.text.startswith("/tozala"):
        queries = []
        await message.reply("List tozalandi")

    else:
        for query in message.text.split():
            await add_query(query)
        


async def loop():
    while True:
        await asyncio.sleep(5)
        query = await pop_query()
        if query:
            try:
                await parser_music(query, clent)
            except Exception as e:
                print(e)



if __name__ == "__main__":
    asyncio.get_event_loop().create_task(loop())
    clent.run()