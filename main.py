import telebot
from yt_dlp import YoutubeDL
import os

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

ydl_opts = {
    'format': 'best',
    'outtmpl': '%(id)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegVideoRemuxer',
        'preferedformat': 'mp4',
    }],
    'noplaylist': True,
    'skip_download': False
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! 🌟 أرسل لي رابط الفيديو الذي تريد تنزيله (يدعم TikTok بدون علامة مائية). 🚀")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            os.remove(filename)  # حذف الملف بعد إرساله
            
    except Exception as e:
        bot.reply_to(message, f"عذرًا، حدث خطأ أثناء تنزيل الفيديو: {e}")

bot.polling(none_stop=True)
