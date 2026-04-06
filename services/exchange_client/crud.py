import requests
import time
from requests.exceptions import Timeout, RequestException, ConnectionError
from typing import Optional


class ExchangeClient:
    def __init__(self, url: str = "https://api.exchangerate-api.com/v4/latest"):
        self.url = url
        self.timeout = 5
        self.max_retries = 3

    def get_exchange_rate(self, base: str, target: str) -> Optional[float]:
        for attempt in range(self.max_retries):
            try:
                response = requests.get(f"{self.url}/{base}", timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                if target in data.get("rates", {}):
                    return data["rates"][target]
                else:
                    print(f"Валюта {target} не найдена!")
                    return None
            except Timeout:
                if attempt < self.max_retries - 1:
                    delay = 2**attempt
                    print(f"Таймаут, повтор через {delay} секунд.")
                    time.sleep(delay)
                else:
                    print("Превышено время ожидания после всех попыток.")
                    return None
            except ConnectionError:
                if attempt < self.max_retries - 1:
                    delay = 2**attempt
                    print(f"Ошибка подключения, повтор через {delay} секунд.")
                    time.sleep(delay)
                else:
                    print("Ошибка подключения после всех попыток.")
                    return None
            except RequestException as e:
                print(f"Ошбика запроса {e}!")
                return None
        return None

    def convert_price(
        self, price: float, from_curr: str, to_curr: str
    ) -> Optional[float]:
        if from_curr == to_curr:
            return price
        rate = self.get_exchange_rate(from_curr, to_curr)
        if rate is None:
            return None
        return rate * price


exchange_client = ExchangeClient()
