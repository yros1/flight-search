import logging
import os
from datetime import date, timedelta
from pathlib import Path

import requests_cache

logger = logging.getLogger(__name__)


class FlightSearch:
    """Search for the cheapest flight deals through the Flights API."""

    def __init__(self):
        """Initialize the Flights API base URL."""
        self.__base_url = "https://app.100daysofpython.dev"

    def get_flights(self, destination_city_code):
        """Return the cheapest flight to the given IATA city code."""
        flight_api_key = os.getenv("FLIGHTS_API_KEY")

        if not flight_api_key:
            logger.error("FLIGHTS_API_KEY environment variable is not set")
            raise RuntimeError("Environment variable FLIGHTS_API_KEY not set")

        endpoint = f"{self.__base_url}/v1/flights/search"

        tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        six_month_from_today = (date.today() + timedelta(days=180)).strftime("%Y-%m-%d")

        parameters = {
            "engine": "google_flights",
            "departure_id": "LHR",
            "arrival_id": destination_city_code,
            "outbound_date": tomorrow,
            "return_date": six_month_from_today,
            "type": 1,
            "adults": 1,
            "currency": "GBP",
            "stops": 1,
            "api_key": flight_api_key,
        }

        cache_path = Path(__file__).parent / "Cache" / "flight_search_cache"
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        session = requests_cache.CachedSession(
            cache_name=cache_path,
            backend="sqlite",
            expire_after=timedelta(hours=12),
        )

        logger.info("Searching flights to %s", destination_city_code)
        response = session.get(url=endpoint, params=parameters, timeout=30)

        response.raise_for_status()
        flights_data = response.json()

        if "error" in flights_data:
            error_message = flights_data["error"]
            logger.error("Flight API returned an error: %s", error_message)
            raise RuntimeError(
                f"Flight API returned error: {error_message}"
            )

        flights = (
            flights_data.get("best_flights", [])
            + flights_data.get("other_flights", [])
        )

        if not flights:
            logger.warning("No flights found for %s", destination_city_code)
            raise RuntimeError(
                f"No flights found for destination {destination_city_code}."
            )

        cheapest = min(flights, key=lambda flight: float(flight["price"]))
        logger.info("Found cheapest flight to %s", destination_city_code)
        return cheapest