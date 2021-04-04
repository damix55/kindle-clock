import kindle
import yaml
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters
from time import sleep
from picture import convert_pic


with open('config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)['telegram']


def photo_handler(update, context):
    msg = update.message
    if msg.chat.username == config['username']:
        pic = msg.photo[-1].get_file()
        download_pic(msg, pic)


def doc_handler(update, context):
    msg = update.message
    if msg.chat.username == config['username']:
        if msg.document.mime_type == 'image/png':
            pic = msg.document.get_file()
            download_pic(msg, pic)

        elif msg.document.mime_type == 'image/jpeg':
            pic = msg.document.get_file()
            download_pic(msg, pic)


def download_pic(msg, pic):
    location = 'tmp/picture.png'
    pic.download(location)
    convert_pic(location, location)
    kindle.show_picture()


def start_bot():
    updater = Updater(config['token'])
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, photo_handler))
    dp.add_handler(MessageHandler(Filters.document, doc_handler))
    updater.start_polling()
    print('Bot started')