import requests
import json
from config import API_KEY, keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f"Недопустимо переводить одинаковые валюты - {base}.")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать переданную валюту - {quote}")
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать переданную валюту - {base}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать переданное количество валюты - {amount}")

        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}")
        total_base = (float(json.loads(r.content)["rates"][base_ticker]) / float(json.loads(r.content)["rates"][quote_ticker])) * amount

        return round(total_base, 1)
