import requests
import os
from telegram.ext import Updater, MessageHandler, Filters
from tqdm import tqdm

TOKEN = '6115652609:AAFEH_kdSQzscIVCQmT7DCUtDiM-jhPVgFI'
CHAT_ID = '@WebTeGram'


def download_file(url):
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    filename = url.split('/')[-1]
    with open(filename, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    return filename


def handle_message(update, context):
    message = update.message
    if message.document or message.photo or message.video or message.audio or message.voice:
        return
    elif message.text.startswith('http'):
        try:
            filename = download_file(message.text)
            with open(filename, 'rb') as f:
                context.bot.send_document(chat_id=CHAT_ID, document=f, caption='Downloaded file')
            os.remove(filename)
        except Exception as e:
            print('Error:', e)


updater = Updater(token=TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.all, handle_message))

updater.start_polling()
updater.idle()
