"""Find low-cost flights and send notifications for matching deals."""

import logging

from dotenv import load_dotenv

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

logger.info("START APP")

load_dotenv()

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

prices = data_manager.get_prices_data()
for price in prices["prices"]:
    destination_city = price["city"]
    destination_city_code = price["iataCode"]
    expected_price = float(price["lowestPrice"])

    logger.info(
        "Checking %s (%s): target price GBP %.2f",
        destination_city,
        destination_city_code,
        expected_price,
    )
    flight = flight_search.get_flights(destination_city_code=destination_city_code)
    cheapest_price = float(flight["price"])
    logger.info("Flight search result for %s: %s", destination_city, flight)
    logger.info(
        "Cheapest flight to %s found for GBP %.2f",
        destination_city,
        cheapest_price,
    )

    departure_airport_IATA_code = flight["flights"][0]["departure_airport"]["id"]
    arrival_airport_IATA_code = flight["flights"][0]["arrival_airport"]["id"]
    departure_airport_time = flight["flights"][0]["departure_airport"]["time"]
    arrival_airport_time = flight["flights"][0]["arrival_airport"]["time"]

    logger.debug("Departure airport IATA code: %s", departure_airport_IATA_code)
    logger.debug("Arrival airport IATA code: %s", arrival_airport_IATA_code)
    logger.debug("Departure airport time: %s", departure_airport_time)
    logger.debug("Arrival airport time: %s", arrival_airport_time)

    flight_data = {
        "departure_airport_IATA_code": departure_airport_IATA_code,
        "destination_airport_IATA_code": arrival_airport_IATA_code,
        "flight_price": cheapest_price,
        "flight_dates": {
            "departure_airport_time": departure_airport_time,
            "arrival_airport_time": arrival_airport_time,
        },
    }

    if cheapest_price < expected_price:
        data_manager.update_lowest_price(
            row_id=price["id"],
            new_lowest_price=cheapest_price,
        )
        notification_manager.send_notification(flight=flight_data)
        logger.info("Updated price and sent notification for %s", destination_city)
    else:
        logger.warning("Cheapest flight price for %s hasn't been found.", destination_city)

logger.info("FINISH APP")