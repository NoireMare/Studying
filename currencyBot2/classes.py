import requests
from config import headers, currencies_all
import json


class UserFaultMessage(Exception):
    pass


class ExchangeConverter:
    pass

    @staticmethod
    def exchange_request(to_: str, from_: str, amount: str, amount_given):
        try:
            if float(amount):
                pass
        except ValueError:
            raise UserFaultMessage(f"Количество '{amount}' какое-то непонятное для меня.")

        try:
            to_value = currencies_all[to_]
        except KeyError:
            raise UserFaultMessage(f"Что-то я ничего не понял про валюту '{to_}'. С чем её едят?")

        try:
            from_value = currencies_all[from_]
        except KeyError:
            raise UserFaultMessage(f"Что-то я ничего не понял про валюту '{from_}'. С чем её едят?")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_value}&from={from_value}&amount={amount}"
        response = requests.request("GET", url, headers=headers)
        result = json.loads(response.content)
        rate = result["result"]

        if amount_given:
            answer = f"Чтобы купить {float(amount_given)} {to_value}, нужно продать \
{round(float(amount_given) / rate, 2)} {from_value}"
        else:
            answer = f"Сегодня и сейчас {amount} {from_value} - это {round(rate, 2)} {to_value}"

        return answer
