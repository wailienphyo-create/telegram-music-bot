import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

app = Client(
    "MusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    session_string=SESSION_STRING if SESSION_STRING else None
)

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("မင်္ဂလာပါ ကိုဖြိုးရေ! Telegram Music Bot အဆင်သင့် ဖြစ်ပါပြီ။")

app.run()
