import json
import requests
from config import exchanges

class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Чечевичка {base} не найдена!")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Чечевичка {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые листочки {base}!')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать {amount} листочков!')

        headers = {"apikey": "DYAakA2Zy5LYwzFLlAsIsoWCUT5unAMH"}
        response = requests.get(f"https://api.apilayer.com/exchangerates_data/latest?base={base_key}&symbols={quote_key}", headers=headers)
        resp = json.loads(response.text)
        new_price = resp['rates'][quote_key] * amount
        new_price = round(new_price, 3)
        message =  f"Цена {amount} {base} в {quote} : {new_price}"
        return message
