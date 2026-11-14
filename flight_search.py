import os
import requests_cache
import sys
from datetime import date, timedelta

requests_cache.install_cache('fligth_search_cache')

class FlightSearch:
    # This a class responsible for talking to the Flight Search API.
    def __init__(self):
        self.base_url = "https://app.100daysofpython.dev"
    """
    Search flights, find the cheapest option, and return the full response.
    """
    def get_flights_data(self, destination_city_code):
        if not os.getenv("FLIGHTS_API_KEY"):
            print("Environment variable 'FLIGHTS_API_KEY' is not set.")
            sys.exit(1)

        endpoint = f"{self.base_url}/v1/flights/search"

        outbound_date = date.today().strftime("%Y-%m-%d")
        return_date = (date.today() + timedelta(days=180)).strftime("%Y-%m-%d")

        parameters = {
            "engine" : "google_flights",
            "departure_id" : "LHR",
            "arrival_id" : destination_city_code,
            "outbound_date" : outbound_date,
            "return_date" : return_date,
            "type" : 1,
            "adults" : 1,
            "currency" : "GBP",
            "stops" : 1,
            "api_key": os.getenv("FLIGHTS_API_KEY")
        }

        session = requests_cache.CachedSession(
            cache_name="fligth_search_cache",
            backend="sqlite",
            expire_after=timedelta(hours=12)
        )

        response = session.get(url=endpoint, params=parameters, timeout=30)

        #print(f"Requesting flight data for destination city code: {destination_city_code}.")

        flights_data = response.json()

        if "error" in flights_data:
            print("API error:", flights_data["error"])
            exit(1)
        else:
            flights = flights_data.get("best_flights", []) + flights_data.get("other_flights", [])
            cheapest = min(flights, key=lambda f: f["price"])
            #print(f"Cheapest flight found for: {cheapest['price']} GBP")
            return cheapest