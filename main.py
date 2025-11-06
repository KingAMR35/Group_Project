import telebot
from config import TOKEN
import time
import nltk
from nltk.corpus import stopwords

bot = telebot.TeleBot(TOKEN)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "Запускает бота🚀"),
        telebot.types.BotCommand("restart", "Перезагрузка бота🔄"),
    ])

nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))
warnings = {}
user_activity = {}
banned_users = {}

MAX_MESSAGES_PER_10_SECONDS = 5

@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Я умный и эффективный бот для Telegram, разработанный для защиты и модерации чатов. Я помогаю поддерживать порядок, безопасность и комфортную атмосферу в вашем сообществе, автоматически отслеживая и устраняя нежелательное поведение.")

@bot.message_handler(commands=["restart"])
def restart_bot(message):
    bot.send_message(message.chat.id, "Идёт перезагрузка, ожидайте🔄")
    time.sleep(1)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Привет, {message.from_user.first_name}! Я умный и эффективный бот для Telegram, разработанный для защиты и модерации чатов. Я помогаю поддерживать порядок, безопасность и комфортную атмосферу в вашем сообществе, автоматически отслеживая и устраняя нежелательное поведение.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.message_id
    words = message.text.lower().split()
    contains_bad_word = False  # Флаг для отслеживания наличия запрещенных слов

    for word in words:
        if word in stop_words:
            contains_bad_word = True
            break  

    if contains_bad_word:
        if user_id in warnings:
            warnings[user_id] += 1
        else:
            warnings[user_id] = 1

        if warnings[user_id] >= 3:
            bot.delete_message(chat_id, message_id)
            bot.send_message(chat_id, f"{message.from_user.first_name} хулиган - получает бан")
            bot.kick_chat_member(chat_id, user_id)
            warnings[user_id] = 0
        else:
            bot.send_message(chat_id, f"{message.from_user.first_name}, пожалуйста, избегайте нецензурной лексики. Это ваше {warnings[user_id]} предупреждение.")

    if user_id in user_activity:
        last_messages_time, message_count = user_activity[user_id]
        current_time = time.time()
        if current_time - last_messages_time > 10:
            user_activity[user_id] = (current_time, 1)
        else:
            message_count += 1
            user_activity[user_id] = (current_time, message_count)

            if message_count >= MAX_MESSAGES_PER_10_SECONDS:
                if user_id in warnings:
                    warnings[user_id] += 1
                else:
                    warnings[user_id] = 1

                if warnings[user_id] >= 3:
                    bot.send_message(chat_id, f"{message.from_user.first_name} хулиган - получает бан")
                    bot.kick_chat_member(chat_id, user_id)
                    warnings[user_id] = 0
                else:
                    bot.send_message(chat_id, f"{message.from_user.first_user.first_name}, пожалуйста, избегайте спама. Это ваше {warnings[user_id]} предупреждение.")
    else:
        user_activity[user_id] = (time.time(), 1)


bot.infinity_polling()