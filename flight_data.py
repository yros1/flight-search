class FlightData:
    """Format flight information for notification messages."""

    @staticmethod
    def format(flight):
        """Return a formatted low-price alert message."""
        message = f"- Low price alert! Only £{flight["flight_price"]} to fly "\
                  f"from {flight["departure_airport_IATA_code"]} "\
                  f"to {flight["destination_airport_IATA_code"]}, "\
                  f"on {flight["flight_dates"]["departure_airport_time"]} "\
                  f"until {flight["flight_dates"]["arrival_airport_time"]}."
        print(message)

        return message