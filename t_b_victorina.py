import random
from telebot import TeleBot, types

# Создаем объект бота, подставив ваш токен
TOKEN = '7782357533:AAHRnFu_7NjxVOX35XSrgHNNV85pu0XbAIU'
bot = TeleBot(TOKEN)

# Вопросы и ответы для разных уровней сложности
questions = {
    'easy': [
        {'question': 'Какое животное является символом России?', 'answer': 'Медведь'},
        {'question': 'Кто быстрее всех бегает среди млекопитающих?', 'answer': 'Гепард'}
    ],
    'medium': [
        {'question': 'Какой хищник считается самым крупным в мире?', 'answer': 'Белый медведь'},
        {'question': 'У какого животного самый длинный хвост относительно тела?', 'answer': 'Мангуст'}
    ],
    'hard': [
        {'question': 'Что такое амблигонит? Это минерал или часть тела у пауков?', 'answer': 'Это минерал'},
        {'question': 'Какие животные обладают способностью менять цвет кожи?', 'answer': 'Хамелеоны'}
    ]
}


# Функция для отправки приветствия и выбора уровня сложности
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = types.KeyboardButton('Легкий')
    itembtn2 = types.KeyboardButton('Средний')
    itembtn3 = types.KeyboardButton('Сложный')
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(
        message.chat.id,
        "Привет! Выбери уровень сложности викторины:",
        reply_markup=markup
    )


# Обработчик сообщений с выбором уровня сложности
@bot.message_handler(func=lambda message: True)
def handle_level_choice(message):
    if message.text == 'Легкий':
        level = 'easy'
    elif message.text == 'Средний':
        level = 'medium'
    else:
        level = 'hard'

    quiz_questions = questions[level]
    current_question = random.choice(quiz_questions)

    # Отправляем первый вопрос
    bot.send_message(message.chat.id, f'Вопрос: {current_question["question"]}')

    @bot.message_handler(content_types=["text"])
    def check_answer(message):
        if message.text.lower() == current_question['answer'].lower():
            bot.send_message(
                message.chat.id,
                "Правильно! Молодец!",
                reply_markup=None
            )

            # Предложение сыграть снова
            markup = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text="Играть еще раз", callback_data='play_again')
            markup.add(button)
            bot.send_message(
                chat_id=message.chat.id, text="Продолжить?", reply_markup=markup
            )
        else:
            bot.send_message(message.chat.id, "Неправильно. Попробуй еще раз.")
            bot.register_next_step_handler(message, check_answer)


# Колбек для кнопки "Играть ещё раз"
@bot.callback_query_handler(func=lambda call: call.data == 'play_again')
def play_again(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Отлично! Начнем заново.')
    send_welcome(call.message)


if __name__ == '__main__':
    bot.polling(none_stop=True)