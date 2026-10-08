import os
import telebot
from yt_dlp import YoutubeDL

API_TOKEN = '8962815799:AAF3xyahDINkSzrXlomn-9bLVtQLQ68i10U'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "မင်္ဂလာပါ! သီချင်းနာမည် သို့မဟုတ် YouTube link ပို့ပေးရင် သီချင်းဒေါင်းလုဒ်ဆွဲပေးပါမယ်။")

@bot.message_handler(func=lambda message: True)
def download_audio(message):
    query = message.text
    msg = bot.reply_to(message, "သီချင်းရှာဖွေပြီး ဒေါင်းလုဒ်ဆွဲနေပါတယ်...")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            if not query.startswith('http'):
                query = f"ytsearch:{query}"
            info = ydl.extract_info(query, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            filename = "song.mp3"
            
        with open(filename, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, title=info.get('title', 'Audio'))
            
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        bot.reply_to(message, f"အမှားအယွင်းရှိနေပါသည်: {str(e)}")

bot.infinity_polling()
