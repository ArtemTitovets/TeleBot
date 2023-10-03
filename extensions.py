import requests
import json
from config import keys


class APIException(Exception):
    pass

class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote} в {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Введено некорректное имя валюты: {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Введено некорректное имя валюты: {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Введено некорректное количество переводимой валюты: {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/7659edaa63a918497ba9d306/pair/{quote_ticker}/{base_ticker}')
        total_base = list((json.loads(r.content)).values())[-1]

        return total_base