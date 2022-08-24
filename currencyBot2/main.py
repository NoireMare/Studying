import telebot
from config import TOKEN, currencies
from classes import ExchangeConverter, UserFaultMessage

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    text = "\nДобро пожаловать!\n\nОчень хочется поменять валюту, купюры аж из штанов торчат, но \
не понятно что почём? Не проблема. Сейчас быстро выясним.\n\n\
Чтобы узнать, например, сколько долларов можно купить на 100 рублей, сделайте следующий запрос \
(одной строкой): <валюта, которую хочется купить> <валюта, которая продаётся> <количество продаваемой \
валюты> .\n\nПокажу вам пример запроса: Доллар рубль 100 .\n\nЧтобы узнать, сколько придётся продать рублей,\
 чтобы купить 100 долларов, сделайте следующий запрос (одной строкой): <cумма, которую вам надо получить \
в итоге> <валюта, которую хочется купить> <валюта, которая продаётся>.\n\nПокажу вам пример запроса: 100 доллар \
рубль.\n\nИспользуйте команду /currencies, чтобы узнать для каких валют доступен расчет конвертации."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["currencies"])
def available_currencies(message: telebot.types.Message):
    text = "Список доступных валют:\n"
    for values in currencies.keys():
        text += f"{values}\n"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def exchange(message: telebot.types.Message):
    try:
        to_, from_, amount, answer, amount_given, flag = [0]*6
        message.text = message.text.lower()
        text = message.text.split()
        if len(text) != 3:
            raise UserFaultMessage(f"Количество элементов в запросе неправильное. Жду 3 отдельных параметра.")
        if "," in text[0]:
            text[0] = text[0].replace(",", ".")
        elif "," in text[2]:
            text[2] = text[2].replace(",", ".")

        try:
            if float(text[0]):
                to_, from_, amount = text[1], text[2], text[0]
                flag = 2
        except ValueError:
            to_, from_, amount = text

        answer = ExchangeConverter.exchange_request(to_, from_, amount, flag)

    except UserFaultMessage as e:
        bot.reply_to(message, f"{e}")
    except Exception:
        bot.reply_to(message, "Что-то биржа поломалась, не делится данными. :( Поехали чинить, а вы зайдите \
попозже, пожалуйста.")

    else:
        bot.send_message(message.chat.id, answer)


bot.polling()
