#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from dotenv import load_dotenv
from data_manager import DataManager
from flight_search import FlightSearch

load_dotenv()

data_manager = DataManager()
print(data_manager.get_prices_data())

flight_search = FlightSearch()
prices = data_manager.get_prices_data()
for price in prices["prices"]:
    destination_city = price["city"]
    destination_city_code = price['iataCode']
    wanted_lowest_price = price["lowestPrice"]

    print(f"\ndestination city: {destination_city}, destination city code: {destination_city_code}, wanted lowest price: {wanted_lowest_price}")
    flight = flight_search.get_flights_data(destination_city_code=destination_city_code)
    print(f"Flight search result data for {destination_city}:\n{flight}")
    print(f"Cheapest flight to for {destination_city} has been found for: {flight['price']} GBP.")