import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SESSION_STRING = os.environ.get("SESSION_STRING")

# Bot & Userbot Clients
bot = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call = PyTgCalls(userbot)

@bot.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply_text("ကျေးဇူးပြု၍ သီချင်းနာမည် သို့မဟုတ် Link ထည့်ပေးပါ။ (ဥပမာ - `/play song name`)")
    
    query = " ".join(message.command[1:])
    msg = await message.reply_text("🔍 သီချင်း ရှာဖွေနေပါသည်...")

    ydl_opts = {"format": "bestaudio/best", "quiet": True}
    with YoutubeDL(ydl_opts) as ydl:
        try:
            results = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            audio_url = results['url']
            title = results['title']
        except Exception as e:
            return await msg.edit_text(f"❌ သီချင်း ရှာမတွေ့ပါ: {e}")

    await msg.edit_text(f"🎵 **{title}** ကို VC ထဲတွင် စတင်ဖွင့်နေပါပြီ...")
    
    try:
        await call.join_group_call(
            message.chat.id,
            AudioPiped(audio_url)
        )
    except Exception as e:
        await msg.edit_text(f"❌ VC ထဲ ဝင်၍မရပါ (VC ပွင့်မပွင့် သို့မဟုတ် Admin power စစ်ပါ): {e}")

async def main():
    await userbot.start()
    await bot.start()
    await call.start()
    print("Bot is running...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
