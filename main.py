# Телеграм бот с игрой Виселица в качестве домашнего задания для школы УмСкул
# 28.11.2023 Максим Елизов

# телебот нужно скачать перед использованием!!
import telebot
import random

# мой токен от бота
bot = telebot.TeleBot("6303106934:AAEixAPQi-mRLLktLKw6tZaI2BbJ3zaZKU0")

# список слов, которые вы будете угадывать (потом будут выбираться случайно)
words = ["умскул", "програмирование", "университет", "интуиция", "ноутбук", "энтузиазм", "автомобиль", "авария", "портфолио", "москва"]

# можете поменять. это количество неправильных попыток для игрока
remaining_guesses = 7
# тут я создаю множество
guessed_letters = set()
word = random.choice(words)
# тут я выбираю случайное слово из него (нашел в интернете, как это пишется в пайтоне)
hidden_word = ["_" for _ in word]

@bot.message_handler(commands=['start'])
def handle_start_command(message):
    # тут я дал доступ к переменным, которые находятся вне функции, а не создал их инстанцию внутри функции
    global remaining_guesses, guessed_letters, word, hidden_word
    remaining_guesses = 7
    # повторяю инициализацию, как и вне функции
    guessed_letters = set()
    word = random.choice(words)
    hidden_word = ["_" for _ in word]
    bot.reply_to(message, "Привет, привет! Это игра Виселица для школы УмСкул! У тебя есть 7 возможностей ошибиться! Снизу слово, смотри внимательно!\n\n" + "".join(hidden_word))

# не совсем понимаю что за lambda, но это позволяет принимать любые сообщения
# (тоже нашел в интернете, все никак не мог сделать нормально)
@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    # тут я снова дал доступ к переменным, которые находятся вне функции, а не создал их инстанцию внутри функции
    global remaining_guesses, guessed_letters, word, hidden_word
    if remaining_guesses <= 0 or "".join(hidden_word) == word:
        return
    if len(message.text) == 1 and message.text.isalpha():
        guess = message.text.lower()
        if guess in guessed_letters:
            bot.send_message(message.chat.id, "Ты уже использовал эту букву, попробуй другую :)")
            return
        guessed_letters.add(guess)
        if guess in word:
            # интересный цикл, который сразу дает индекс буквы и саму букву
            for i, letter in enumerate(word):
                if guess == letter:
                    hidden_word[i] = guess
        else:
            remaining_guesses = remaining_guesses - 1
        bot.send_message(message.chat.id, "У тебя осталось " + str(remaining_guesses) + " неправильных попыток.\n\n" + "".join(hidden_word))
        if "".join(hidden_word) == word:
            bot.send_message(message.chat.id, "Поздравляю! Ты угадал, загаданное слово!\n\nЭто было слово: " + word + "\nНапиши /start, чтобы начать снова!")
        elif remaining_guesses <= 0:
            bot.send_message(message.chat.id, "Ты проиграл :( \nСлово было: " + word + "\nНапиши /start, чтобы начать снова!")
    else:
        bot.send_message(message.chat.id, "Неправильно что-то написал. Нужно букву писать, хе-хе!")

bot.infinity_polling()

# Наблюдения: Наткнулся на следующий баг. Когда я дал бота протестировать своему другу, и мы
# одновременно угадывали буквы в игре, то эти буквы угадывались и у меня, или наоборот мне считались
# его неправильные попытки. Хотелось бы очень это исправить, но не успеваю :(
