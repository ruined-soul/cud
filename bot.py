import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import filters
import requests
import os

# Replace with your actual Telegram bot token
TELEGRAM_TOKEN = '7304879730:AAGYfEoYWKeUW9-bP3wQ6UNHhzRthkSUxU0'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi there, I am an uploader.')

async def handle_document(update: Update, context: CallbackContext) -> None:
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
                await update.message.reply_text(f'File uploaded to Telegraph: https://telegra.ph{file_url}')
            else:
                await update.message.reply_text('Failed to upload file.')
        else:
            await update.message.reply_text('Error uploading file.')
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        await update.message.reply_text('An error occurred while processing the file.')

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Use filters.Document() to filter document messages
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    application.run_polling()

if __name__ == '__main__':
    main()
