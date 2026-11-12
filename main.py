#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from dotenv import load_dotenv
from data_manager import DataManager

load_dotenv()

data_manager = DataManager()
print(data_manager.get_prices_data())