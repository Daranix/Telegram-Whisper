import whisper
import os
from telegram import Update, Bot, File as TelegramFile, Audio, Voice
from telegram.ext import MessageHandler, filters, CommandHandler, CallbackContext, Application
from dotenv import load_dotenv
import tempfile
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

logger.info("Downloading model ... ")
model = whisper.load_model("base")

logger.info("Model downloaded")


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Send a audio to transcript")


async def proccessAudio(update: Update, context: CallbackContext):
    #result = model.transcribe("audio.ogg")
    logger.info("Proccessing new audio")
    audio_file: TelegramFile = None
    if update.message.audio:
        audio_file = await update.message.audio.get_file()
    elif update.message.voice:
        audio_file = await update.message.voice.get_file()
    else:
        await update.message.reply_text("Invalid audio format")
        return

    # download the voice note as a file
    ftemp = tempfile.NamedTemporaryFile()
    await audio_file.download(out=ftemp)
    await update.message.reply_text("Your audio is processing ... wait a few seconds")
    result = model.transcribe(ftemp.name)
    ftemp.close()
    await update.message.reply_text(result["text"])


def main():
    load_dotenv()
    TOKEN = os.environ.get('TOKEN')
    PORT = int(os.environ.get('PORT', '8443'))
    PROFILE = os.environ.get('PROFILE', 'dev')
    APP_URL = os.environ.get('APP_URL')
    application = Application.builder().token(TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start))

    # Start checking updates
    application.add_handler(MessageHandler(
        filters.VOICE | filters.Document.AUDIO | filters.ATTACHMENT, proccessAudio))

    # Log errors
    # dp.add_error_handler(error)

    logger.info("Starting telegram bot")

    # start the bot
    if PROFILE == 'prod':
        application.run_webhook(listen="0.0.0.0",
                                port=PORT,
                                url_path=TOKEN,
                                webhook_url=APP_URL + TOKEN)
    else:
        application.run_polling()


if __name__ == '__main__':
    main()
