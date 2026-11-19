import logging
import os
from datetime import timedelta
from pathlib import Path

import requests
import requests_cache

logger = logging.getLogger(__name__)


class DataManager:
    """Retrieve and update flight prices using the Sheety API."""

    def __init__(self):
        """Initialize the API credentials and Sheety base URL."""
        self.__base_url = "https://api.sheety.co"
        self.__username = os.getenv("YOUR_SHEETY_API_USERNAME")
        self.__authentication_bearer_token = os.getenv(
            "YOUR_SHEETY_API_AUTHENTICATION_BEARER_TOKEN"
        )

        if not self.__username:
            logger.error("YOUR_SHEETY_API_USERNAME environment variable is not set")
            raise RuntimeError("Environment variable YOUR_SHEETY_API_USERNAME is not set")

        if not self.__authentication_bearer_token:
            logger.error(
                "YOUR_SHEETY_API_AUTHENTICATION_BEARER_TOKEN environment variable is not set"
            )
            raise RuntimeError(
                "Environment variable YOUR_SHEETY_API_AUTHENTICATION_BEARER_TOKEN is not set"
            )

    def get_prices_data(self):
        """Retrieve destination and lowest-price data from the Google Sheet."""
        endpoint = f"{self.__base_url}/{self.__username}/flightDeals/prices"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{self.__authentication_bearer_token}",
        }

        cache_path = Path(__file__).parent / "Cache" / "sheety_prices_cache"
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        session = requests_cache.CachedSession(
            cache_name=cache_path,
            backend="sqlite",
            expire_after=timedelta(hours=12),
        )

        logger.info("Retrieving destination prices from Sheety")
        response = session.get(url=endpoint, timeout=5, headers=headers)

        response.raise_for_status()
        prices_data = response.json()
        logger.info("Retrieved destination price data")
        return prices_data

    def update_lowest_price(self, row_id, new_lowest_price):
        """Update the lowest price for one row in the Google Sheet."""
        body = {
            "price": {
                "lowestPrice": new_lowest_price,
            },
        }

        endpoint = f"{self.__base_url}/{self.__username}/flightDeals/prices/{row_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{self.__authentication_bearer_token}",
        }

        logger.info("Updating lowest price for row %s to GBP %.2f", row_id, new_lowest_price)
        response = requests.put(
            url=endpoint,
            json=body,
            timeout=5,
            headers=headers,
        )

        response.raise_for_status()
        logger.info("Lowest price updated for row %s", row_id)

