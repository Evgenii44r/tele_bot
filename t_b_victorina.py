import telebot
from telebot import types

# Ваш токен API, полученный от BotFather
API_TOKEN = '7782357533:AAHRnFu_7NjxVOX35XSrgHNNV85pu0XbAIU'

# Создаем объект TeleBot
bot = telebot.TeleBot(API_TOKEN)

# Список уровней сложности
levels = ["Легкий", "Средний", "Сложный"]

# Вопросы для каждого уровня
questions = {
    "Легкий": [("Самое быстрое животное в мире?",'Гепард'),( "Какое животное обитает только в Китае?",'Панда')],
    "Средний": [("Какая  птица  умеет летать?",'Пингвин'), ("Какую еду большие панды предпочитают любой другой?", 'Бамбук')],
    "Сложный": [("как быстро могут бегать страусы?",'70км в час'), (" Какого цвета кожа полярного медведя?",'Черная')]
}

# Словарь для хранения текущего состояния пользователя
user_state = {}


# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Давай начнем викторину. Выберите уровень сложности:")
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for level in levels:
        keyboard.add(level)
    bot.send_message(message.chat.id, "Выберите уровень:", reply_markup=keyboard)


# Обработчик выбора уровня сложности
@bot.message_handler(func=lambda message: message.text in levels)
def select_level(message):
    user_state[message.chat.id] = {"level": message.text, "current_question": 0}
    ask_question(message)


# Функция для отправки вопроса
def ask_question(message):
    level = user_state[message.chat.id]["level"]
    question_number = user_state[message.chat.id]["current_question"]
    question, _ = questions[level][question_number]
    bot.send_message(message.chat.id, f"Вопрос: {question}")


# Обработчик ответов на вопросы
@bot.message_handler(func=lambda message: message.chat.id in user_state)
def handle_answer(message):
    level = user_state[message.chat.id]["level"]
    question_number = user_state[message.chat.id]["current_question"]
    _, correct_answer = questions[level][question_number]

    if message.text.lower() == correct_answer.lower():
        bot.send_message(message.chat.id, "Верно! Молодец!")
    else:
        bot.send_message(message.chat.id, f"Неверно. Правильный ответ: {correct_answer}")

    if question_number < len(questions[level]) - 1:
        user_state[message.chat.id]["current_question"] += 1
        ask_question(message)
    else:
        del user_state[message.chat.id]
        bot.send_message(message.chat.id, "Викторина завершена! Спасибо за участие.")


if __name__ == '__main__':
    # Запускаем бесконечный цикл обработки событий
    bot.polling()