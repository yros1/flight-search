"""Find low-cost flights and send notifications for matching deals."""

from dotenv import load_dotenv

from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

load_dotenv()

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

prices = data_manager.get_prices_data()
for price in prices["prices"]:
    destination_city = price["city"]
    destination_city_code = price["iataCode"]
    expected_price = float(price["lowestPrice"])

    print(f"\ndestination city: {destination_city}, destination city code: {destination_city_code}, expected price: {expected_price}")
    flight = flight_search.get_flights(destination_city_code=destination_city_code)
    cheapest_price = float(flight["price"])
    print(f"Flight search result data for {destination_city}:\n{flight}")
    print(f"Cheapest flight to {destination_city} has been found for: {cheapest_price} GBP.")

    departure_airport_IATA_code = flight["flights"][0]["departure_airport"]["id"]
    arrival_airport_IATA_code = flight["flights"][0]["arrival_airport"]["id"]
    departure_airport_time = flight["flights"][0]["departure_airport"]["time"]
    arrival_airport_time = flight["flights"][0]["arrival_airport"]["time"]

    print(f"\nDeparture airport time: {departure_airport_IATA_code}")
    print(f"Arrival airport time: {arrival_airport_IATA_code}")
    print(f"\nDeparture airport time: {departure_airport_time}")
    print(f"Arrival airport time: {arrival_airport_time}")

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