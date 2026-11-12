import os
import requests_cache
import sys
from datetime import timedelta

requests_cache.install_cache('sheety_cache')

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        # https://api.sheety.co/your_sheety_api_username_here/flightDeals/prices
        self.base_url = "https://api.sheety.co"

    def get_prices_data(self):
        if not os.getenv("YOUR_SHEETY_API_USERNAME"):
            print("Environment variable 'YOUR_SHEETY_API_USERNAME' is not set.")
            sys.exit(1)
        if not os.getenv("YOUR_SHEETY_API_AUTHENTICATION_BEARER_TOKEN"):
            print("Environment variable 'YOUR_SHEETY_API_AUTHENTICATION_BEARER_TOKEN' is not set.")
            sys.exit(1)

        endpoint = f"{self.base_url}/{os.getenv('YOUR_SHEETY_API_USERNAME')}/flightDeals/prices"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{os.getenv('YOUR_SHEETY_API_AUTHENTICATION_BEARER_TOKEN')}"
        }

        session = requests_cache.CachedSession(
            cache_name="sheety_prices_cache",
            backend='sqlite',
            expire_after=timedelta(hours=12),
        )

        response = session.get(url=endpoint, timeout=5, headers=headers)

        response.raise_for_status()
        prices_data = response.json()

        return prices_data
    pass