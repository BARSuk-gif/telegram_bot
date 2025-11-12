
import random
import bd_functions
from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
import configparser


config = configparser.ConfigParser()
config.read("settings.ini")

print('Start telegram bot...')

state_storage = StateMemoryStorage()
token_bot = config['telegram']['token']
bot = TeleBot(token_bot, state_storage=state_storage)


known_users = set()
userStep = {}
buttons = []


def show_hint(*lines):
    return '\n'.join(lines)


def show_target(data):
    return f"{data['target_word']} -> {data['translate_word']}"


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово 🔙'
    NEXT = 'Дальше ⏭'


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        print(f'Обнаружен новый пользовательс id {uid}')
        return 0


@bot.message_handler(commands=['cards', 'start'])
def create_cards(message):
    cid = message.chat.id
    user_name = message.from_user.first_name or "Пользователь"

    bd_functions.register_user(cid, user_name)

    if cid not in known_users:
        known_users.add(cid)
        userStep[cid] = 0

        pr_text = """Привет 👋 Давай попрактикуемся в английском языке. 
Тренировки можешь проходить в удобном для себя темпе.
У тебя есть возможность использовать тренажёр, как конструктор,
и собирать свою собственную базу для обучения. 
Для этого воспользуйся инструментами:
- добавить слово ➕
- удалить слово 🔙

Ну что, начнём ⬇️"""

        bot.send_message(cid, pr_text)

    markup = types.ReplyKeyboardMarkup(row_width=2)

    # Получаем слова
    target_word_obj = bd_functions.get_target_word(cid)
    translate_word = bd_functions.get_translate_word(target_word_obj)
    others = bd_functions.get_others_words(target_word_obj)

    # Создаем кнопки
    buttons = []

    correct_translate_btn = types.KeyboardButton(translate_word)
    buttons.append(correct_translate_btn)
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)

    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)

    greeting = f"Укажите правильный перевод слова:\n🇷🇺 {target_word_obj.target_word}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)

    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word_obj.target_word
        data['translate_word'] = translate_word
        data['other_words'] = others
        # Сохраняем объект для операций
        data['target_word_obj'] = target_word_obj
        # Сохраняем текущие кнопки перевода в состоянии
        data['current_translate_buttons'] = [translate_word] + others

@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    create_cards(message)


@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):
    cid = message.chat.id

    # Получаем количество активных слов из базы
    active_word_count = bd_functions.session.query(bd_functions.User_Target_Relations).filter(
        bd_functions.User_Target_Relations.user_id == cid,
        bd_functions.User_Target_Relations.is_active == True
    ).count()

    if active_word_count <= 5:
        bot.send_message(
            cid,
            f"Нельзя удалить слово. У вас должно остаться 5 слов для обучения. \n"
            f"Сейчас у вас {active_word_count} слов. Добавьте новые слова перед удалением"
        )
        return
    
    # Спрашиваем пользователя, какое слово он хочет удалить
    bot.send_message(
        cid, "Введите слово на русском языке, которое хотите удалить:")
    bot.register_next_step_handler(message, process_delete_word)


def process_delete_word(message):
    cid = message.chat.id
    word_to_delete = message.text.strip()
    
    # Проверяем, существует ли такое слово у пользователя
    user_words = bd_functions.session.query(bd_functions.Target_words).join(
        bd_functions.User_Target_Relations,
        bd_functions.Target_words.id == bd_functions.User_Target_Relations.target_id
    ).filter(
        bd_functions.User_Target_Relations.user_id == cid,
        bd_functions.User_Target_Relations.is_active == True,
        bd_functions.Target_words.target_word == word_to_delete
    ).first()

    if not user_words:
        bot.send_message(
            cid, f"❌ Слово '{word_to_delete}' не найдено в вашей коллекции.")
        create_cards(message)
        return
    
    # Удаляем слово из БД
    if bd_functions.delete_user_word(cid, word_to_delete):
        bot.send_message(cid, f"✅ Слово '{word_to_delete}' успешно удалено!")
        # Обновляем карточки после удаления
        create_cards(message)
    else:
        bot.send_message(cid, f"❌ Не удалось удалить слово '{word_to_delete}'")
        create_cards


@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    cid = message.chat.id    

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']
        translate_word = data['translate_word']
        others = (data['other_words'])

        # Создаем новое слово, которое пользователь хочет добавить
        bot.send_message(
            cid, "Введите слово на русском языке, которое хотите добавить:")
        bot.register_next_step_handler(message, process_target_word)

def process_target_word(message):
    cid = message.chat.id
    user_target_word = message.text
    bot.send_message(
        cid, f"Введите правильный перевод для слова '{user_target_word}':")
    bot.register_next_step_handler(
        message, process_translate_word, user_target_word)
    
def process_translate_word(message, user_target_word):
    cid = message.chat.id
    user_translate_word = message.text
    bot.send_message(
        cid, f"Введите первый вариант неправильного перевода для слова '{user_target_word}':")
    bot.register_next_step_handler(
        message, process_other_word1, user_target_word, user_translate_word)
    
def process_other_word1(message, user_target_word, user_translate_word):
    cid = message.chat.id
    other_word1 = message.text
    bot.send_message(
        cid, f"Введите второй вариант неправильного перевода для слова '{user_target_word}':")
    bot.register_next_step_handler(
        message, process_other_word2, user_target_word, user_translate_word, other_word1)
    

def process_other_word2(message, user_target_word, user_translate_word, other_word1):
    cid = message.chat.id
    other_word2 = message.text

    bot.send_message(
        cid, f"Введите третий вариант неправильного перевода для слова '{user_target_word}':")
    bot.register_next_step_handler(
        message, process_other_word3, user_target_word, 
        user_translate_word, other_word1, other_word2
        )


def process_other_word3(message, user_target_word, user_translate_word, 
                        other_word1, other_word2):
    cid = message.chat.id
    other_word3 = message.text

    # # Добавляем слово в БД
    if bd_functions.add_user_word(cid, user_target_word, user_translate_word,
                                  other_word1, other_word2, other_word3):
        bot.send_message(
            cid, f"✅ Слово '{user_target_word}' успешно добавлено в вашу коллекцию!")
    else:
        bot.send_message(
            cid, f"❌ Не удалось добавить слово '{user_target_word}'")
        
    create_cards(message)
    

@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    text = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        translate_word = data['translate_word']
        current_translate_buttons = data.get('current_translate_buttons', [])

        # Создаем базовые кнопки команд
        next_btn = types.KeyboardButton(Command.NEXT)
        add_word_btn = types.KeyboardButton(Command.ADD_WORD)
        delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
        command_buttons = [next_btn, add_word_btn, delete_word_btn]

        if text == translate_word:
            # Правильный ответ
            hint = show_target(data)
            hint_text = ["✅ Отлично! ❤", hint]
            buttons = command_buttons
            hint = show_hint(*hint_text)
        else:
            # Неправильный ответ
            new_buttons = []
            for btn_text in current_translate_buttons:
                if btn_text == text:
                    new_btn= types.KeyboardButton(btn_text + ' ❌')
                    new_buttons.append(new_btn)
                else:
                    new_btn = types.KeyboardButton(btn_text)
                    new_buttons.append(new_btn)

            # Перемешиваем кнопки снова
            random.shuffle(new_buttons)
            # Добавляем кнопки команд
            buttons = new_buttons + command_buttons
            hint = show_hint("❌ Допущена ошибка!",
                             f"Попробуй ещё раз вспомнить слово 🇷🇺{data['target_word']}")

    markup.add(*buttons)
    bot.send_message(message.chat.id, hint, reply_markup=markup)


if __name__ == "__main__":
    print("Запуск бота...")
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling(skip_pending=True)
    print("Бот остановлен")
