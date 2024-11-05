from decimal import Decimal

import requests


class NPBApiClient:
    base_url = "https://api.nbp.pl/api/"
    table = "a"

    def __init__(self):
        self.session = requests.Session()

    def get_currency(self, code):
        try:
            response = self.session.get(f"{self.base_url}exchangerates/rates/{self.table}/{code.value}")
            response.raise_for_status()
            rates = response.json().get("rates", [])
            return rates[0].get("mid")
        except requests.exceptions.RequestException as e:
            print(f"Failed to get currency for {code}")
            raise e

    def convert_to(self, code, value):
        current_value = self.get_currency(code)
        return float((Decimal(value) / Decimal(current_value)).quantize(Decimal("0.00")))
