import requests
import json
from bot_info import keys

class APIException(Exception):
    pass

class GetPrice:
    @staticmethod
    def exch(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException('Невозможно перевести одинаковые валюты.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        
        # r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=e32cba038a638164d6bae43444a4ddb6&base={quote_ticker}&symbols={base_ticker}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base_exch = json.loads(r.content)[keys[base]]*amount
        return total_base_exch