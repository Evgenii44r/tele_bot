import telebot

# Вставьте сюда ваш токен от BotFather
API_TOKEN = '7612895744:AAEfYIBeHSt1ueaKa5jnOeWy1P48ky3lKFo'

# Создаем объект бота
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Привет! И тебе всего хорошего!!!")

if __name__ == '__main__':
    # Запускаем бесконечный цикл обработки сообщений
    bot.polling()
