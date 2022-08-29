import telebot
from telebot import types

from config import TOKEN, currencies, currencies_all, request
from classes import ExchangeConverter

bot = telebot.TeleBot(TOKEN)


def keyboard_input(from_):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for values in currencies.keys():
        if values != from_:
            buttons.append(types.KeyboardButton(values))
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    text = "\nДобро пожаловать!\n\nОчень хочется поменять валюту, купюры аж из штанов торчат, но \
не понятно что почём? Не проблема. Сейчас быстро выясним.\n\n\
Чтобы узнать, сколько валюты можно купить на определённое количество другой валюты, \
воспользуйтесь коммандой /one.\n\nЧтобы рассчитать, сколько придётся продать одной валюты, чтобы \
купить определённое количество другой, выберите комманду /two.\
\n\nИспользуйте команду /currencies, чтобы узнать для каких валют доступен расчет конвертации."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["currencies"])
def available_currencies(message: telebot.types.Message):
    text = "Список доступных валют:\n"
    for values in currencies.keys():
        text += f"{values}\n"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["one"])
def one(message: telebot.types.Message):
    request["flag"] = 1
    text = "Какую валюту будем менять?"
    bot.send_message(message.chat.id, text, reply_markup=keyboard_input(0))
    bot.register_next_step_handler(message, from_currency)


@bot.message_handler(commands=["two"])
def two(message: telebot.types.Message):
    request["flag"] = 2
    text = "С какой валютой прощаемся?"
    bot.send_message(message.chat.id, text, reply_markup=keyboard_input(0))
    bot.register_next_step_handler(message, from_currency)


@bot.message_handler(content_types=["text"])
def from_currency(message: telebot.types.Message):
    from_ = 0
    try:
        from_ = message.text.strip().lower()
        request["from_value"] = currencies_all[from_]
    except KeyError:
        bot.send_message(message.chat.id, f"Что-то я ничего не понял про валюту '{from_}'. С чем её едят?")
        bot.register_next_step_handler(message, from_currency)
    else:
        text = "На какую валюту меняем?"
        bot.send_message(message.chat.id, text, reply_markup=keyboard_input(from_))
        bot.register_next_step_handler(message, to_currency)


def to_currency(message: telebot.types.Message):
    to_ = 0
    question = ""
    try:
        to_ = message.text.strip().lower()
        request["to_value"] = currencies_all[to_]
    except KeyError:
        bot.send_message(message.chat.id, f"Что-то я ничего не понял про валюту '{to_}'. С чем её едят?")
        bot.register_next_step_handler(message, to_currency)
    else:
        if request["flag"] == 1:
            question = f"Какую сумму {request['from_value']} продаём?"
        elif request["flag"] == 2:
            question = f"Какая сумма в {request['to_value']} должна быть куплена?"
        bot.send_message(message.chat.id, question)
        bot.register_next_step_handler(message, amount_total)


def amount_total(message: telebot.types.Message):
    amount = 0
    try:
        amount = message.text.strip()
        if "," in amount:
            amount = amount.replace(",", ".")
        if float(amount):
            request["amount"] = amount
    except ValueError:
        bot.reply_to(message, f"Количество '{amount}' какое-то непонятное для меня.")
        bot.register_next_step_handler(message, amount_total)
    else:
        try:
            answer = ExchangeConverter.exchange_request(request["to_value"], request["from_value"], request["amount"], request["flag"])
            for val in request.keys():
                request[val] = 0
        except Exception:
            bot.reply_to(message, "Что-то биржа поломалась, не делится данными. :( Поехали чинить, а вы зайдите \
    #попозже, пожалуйста.")
        else:
            bot.send_message(message.chat.id, answer)


bot.polling()
