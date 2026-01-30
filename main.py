import asyncio, os, sys
from pyrogram import Client, filters
from pyrogram.types import Message
from loader import clent, add_audio, update_search_message
from parser import parser_music



@clent.on_message(filters.animation)
async def message_handler(client: Client, message: Message):
    if message.chat.username != "Music_to_you_bot":
        return

    if message.caption.startswith("🎧"):
        await update_search_message(message)


@clent.on_message(filters.audio)
async def copy_music(client: Client, message: Message):
    if message.chat.username != "Music_to_you_bot":
        return

    await add_audio(message)
    

async def loop():
    with open("musics.txt") as f:
        text = f.read()
    await asyncio.sleep(5)
    queries = [query.strip() for query in text.split("\n") if query.strip()]
    
    for index, query in enumerate(queries):
        print(index+1, query)
        try:
            await parser_music(query, clent)
        except Exception as e:
            print("loop:", e)


    await clent.stop()
    raise SystemExit()



if __name__ == "__main__":
    asyncio.get_event_loop().create_task(loop())
    clent.run()