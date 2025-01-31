from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os
import ast
from dotenv import load_dotenv

load_dotenv()


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AUTHORIZED_TELEGRAM_USERS = ast.literal_eval(os.getenv('AUTHORIZED_USERS'))
API_AUTHORIZED_TOKEN = ast.literal_eval(os.getenv('AUTHORIZED_TOKENS'))[0]


def is_valid_imei(imei):
    return len(imei) == 15 and imei.isdigit()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Отправьте мне IMEI для проверки.')


async def handle_imei(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user.username
    if user not in AUTHORIZED_TELEGRAM_USERS:
        await update.message.reply_text('Вы не авторизованы для использования этого бота.')
        return

    imei = update.message.text
    if not is_valid_imei(imei):
        await update.message.reply_text('Неверный IMEI. Проверьте и отправьте снова.')
        return

    response = requests.post(
        'http://localhost:5000/api/check-imei',
        json={'imei': imei, 'token': API_AUTHORIZED_TOKEN}
    )

    imei_info = response.json()
    await update.message.reply_text(str(imei_info))


def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    imei_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_imei)

    application.add_handler(start_handler)
    application.add_handler(imei_handler)

    application.run_polling()


if __name__ == '__main__':
    print('Бот запущен')
    main()