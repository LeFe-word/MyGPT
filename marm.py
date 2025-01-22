from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
import configparser

# Настройки API
# TELEGRAM_TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"
# OPENAI_API_KEY = "ВАШ_КЛЮЧ_API_ОТ_OPENAI"

# Настройка OpenAI
openai.api_key = 0
# OPENAI_API_KEY

# Ответ на сообщение
def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я твоя мармеладная. Напиши что-нибудь, пошепчемся!")

# Обработка сообщений
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    try:
        bot_response = chat_with_gpt(user_message)
        update.message.reply_text(bot_response)
    except Exception as e:
        update.message.reply_text("Ошибка при обработке запроса: " + str(e))

# Основная функция
def main():
    # Создаем объект ConfigParser
    config = configparser.ConfigParser()

    # Читаем файл конфигурации
    config.read("send.ini")

    try:
        # Извлекаем данные из секции [Telegram]
        token = config["Telegram"]["token"]
        openai.api_key = config["Telegram"]["api_key"]
        # log_file = config["Telegram"]["log_file"]
    except KeyError as e:
        print(f"Error: Missing configuration parameter: {e}")
        return

  
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
