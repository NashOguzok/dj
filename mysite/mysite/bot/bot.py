from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Токен вашего бота
TOKEN = '7609083202:AAHxWuQatfnU8c-SdjfEH6Qapd_2lvAaIW4'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я могу скачать медиафайл из ссылки.')

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Отправь мне ссылку на медиафайл, и я постараюсь его скачать.')

def download_file(update: Update, context: CallbackContext):
    # Получаем сообщение от пользователя
    message = update.message.text
    
    # Проверяем, является ли ссылка валидной
    if not is_valid_url(message):
        update.message.reply_text("Пожалуйста, предоставьте корректную ссылку.")
        return
    
    # Скачиваем файл
    file_path = download_media(message)
    
    if file_path:
        with open(file_path, 'rb') as f:
            update.message.reply_document(f)
        
        # Удаление файла после отправки
        os.remove(file_path)
    else:
        update.message.reply_text("Не удалось скачать файл.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

import re

def is_valid_url(url):
    pattern = r'https?://(?:[-\w.]|%[0-9A-Fa-f]{2})+(?::\d+)?/.*'
    return bool(re.match(pattern, url))

import youtube_dl

def download_media(url):
    ydl_opts = {
        'outtmpl': '/tmp/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
    }
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            ydl.download([url])
            
            # Возвращаем путь к загруженному файлу
            return f'/tmp/{video_title}.{info_dict["ext"]}'
    except exception as e:
        print(f'Ошибка при загрузке: {e}')
        return None
