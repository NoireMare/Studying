import requests
from config import headers, request
import json


class ExchangeConverter:
    pass

    @staticmethod
    def exchange_request(to_: str, from_: str, amount: str, flag: int):
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_}&from={from_}&amount={amount}"
        response = requests.request("GET", url, headers=headers)
        result = json.loads(response.content)
        rate = result["result"]

        if request["flag"] == 2:
            answer = f"Чтобы купить {float(amount)} {to_}, нужно продать \
{round(float(amount)**2 / rate, 2)} {from_}"
        else:
            answer = f"Сегодня и сейчас {amount} {from_} - это {round(rate, 2)} {to_}"

        return answer
