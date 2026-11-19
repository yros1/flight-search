# Flight Deals Search

A Python application that searches for flight deals, compares them with target prices stored in a Google Sheet, and sends a WhatsApp notification when a lower fare is found.

## Features

- Retrieves destinations and target prices through the Sheety API
- Searches for flights using the Flights API
- Finds the cheapest available flight
- Updates the Google Sheet when a lower fare is found
- Sends flight deal notifications through Twilio WhatsApp
- Caches API responses using SQLite

## Technologies

- Python
- Requests
- Requests-Cache
- Twilio
- python-dotenv
- Sheety API
- Flights API

## Project Structure

```text
flight-search/
├── main.py
├── data_manager.py
├── flight_search.py
├── flight_data.py
├── notification_manager.py
├── Cache/
└── requirements.txt
```

## Environment Variables

Create a `.env` file in the project directory:

```env
YOUR_SHEETY_API_USERNAME=your_sheety_username
YOUR_SHEETY_API_AUTHENTICATION_BEARER_TOKEN=your_sheety_token
FLIGHTS_API_KEY=your_flights_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+123456789
TWILIO_WHATSAPP_TO=whatsapp:+123456789
```

Never commit `.env` or API credentials.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

```powershell
python main.py
```

The application:

1. Loads destinations and target prices from Google Sheets.
2. Searches for a flight to each destination.
3. Compares the cheapest fare with the stored target price.
4. Updates the sheet when a lower fare is found.
5. Sends a WhatsApp notification containing the flight details.

## Cache

API responses are cached in SQLite database files inside the `Cache` directory to reduce repeated API calls.

## License

See the `LICENSE` file for license information.
