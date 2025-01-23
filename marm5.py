from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
import configparser
import os

# Чтение конфигурации из файла gpt.ini
config = configparser.ConfigParser()
config.read('gpt.ini')

TELEGRAM_TOKEN = config['Telegram']['TOKEN']
OPENAI_API_KEY = config['OpenAI']['API_KEY']
ALLOWED_USERS = list(map(int, config['Access']['ALLOWED_USERS'].split(',')))

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Хранилище контекстов диалогов
user_contexts = {}

# Ответ на сообщение через OpenAI API
def chat_with_gpt(user_id, dialog_index, user_message):
    if user_id not in user_contexts:
        user_contexts[user_id] = {i: [] for i in range(1, 6)}
    
    context = user_contexts[user_id][dialog_index]
    context.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=context
        )
        bot_message = response['choices'][0]['message']['content']
        context.append({"role": "assistant", "content": bot_message})
        return bot_message
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Проверка доступа
def check_access(update: Update):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        update.message.reply_text("Камзол ещё не сshit. Куды прешь?")
        return False
    return True

# Команда /start
def start(update: Update, context: CallbackContext):
    if not check_access(update):
        return
    user_id = update.effective_user.id
    user_contexts[user_id] = {i: [] for i in range(1, 6)}
    context.user_data['current_dialog'] = 1
    update.message.reply_text("Привет! Я твоя мармеладная. Напиши что-нибудь, пошепчемся!")

# Сброс текущего диалога
def reset(update: Update, context: CallbackContext):
    if not check_access(update):
        return
    user_id = update.effective_user.id
    dialog_index = context.user_data.get('current_dialog', 1)
    user_contexts[user_id][dialog_index] = []
    update.message.reply_text(f"Контекст диалога {dialog_index} сброшен.")

# Переключение диалога
def switch_dialog(update: Update, context: CallbackContext):
    if not check_access(update):
        return
    try:
        dialog_index = int(context.args[0])
        if dialog_index < 1 or dialog_index > 5:
            raise ValueError
        context.user_data['current_dialog'] = dialog_index
        update.message.reply_text(f"Переключен на диалог {dialog_index}.")
    except (IndexError, ValueError):
        update.message.reply_text("Пожалуйста, укажите номер диалога от 1 до 5. Пример: /switch 3")

# Обработка сообщений
def handle_message(update: Update, context: CallbackContext):
    if not check_access(update):
        return
    user_id = update.effective_user.id
    dialog_index = context.user_data.get('current_dialog', 1)
    user_message = update.message.text
    bot_response = chat_with_gpt(user_id, dialog_index, user_message)
    update.message.reply_text(bot_response)

# Основная функция
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(CommandHandler("switch", switch_dialog))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
