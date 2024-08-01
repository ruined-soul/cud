import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

# Replace with your actual Telegram bot token
TELEGRAM_TOKEN = '7304879730:AAE71ZB-KQNB4_-yOTYTZbwLLKP78TjJFYg'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi there, I am an uploader.')

def handle_document(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    file.download('temp_file')

    # Upload file to Telegraph
    try:
        with open('temp_file', 'rb') as f:
            response = requests.post(
                'https://telegra.ph/upload',
                files={'file': f}
            )
            
        os.remove('temp_file')  # Clean up the temp file

        if response.status_code == 200:
            data = response.json()
            if 'src' in data[0]:
                file_url = data[0]['src']
                update.message.reply_text(f'File uploaded to Telegraph: https://telegra.ph{file_url}')
            else:
                update.message.reply_text('Failed to upload file.')
        else:
            update.message.reply_text('Error uploading file.')
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        update.message.reply_text('An error occurred while processing the file.')

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
