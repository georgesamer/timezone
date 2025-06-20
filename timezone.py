# Simple Chatbot for Country Time and Time Difference
import pytz
from timezonefinder import TimezoneFinder
from datetime import datetime

# A mapping of country names to their capital cities (for simplicity)
COUNTRY_CAPITALS = {
    'egypt': 'Cairo',
    'united states': 'Washington',
    'usa': 'Washington',
    'france': 'Paris',
    'germany': 'Berlin',
    'japan': 'Tokyo',
    'china': 'Beijing',
    'india': 'New Delhi',
    'brazil': 'Brasilia',
    'canada': 'Ottawa',
    'australia': 'Canberra',
    'russia': 'Moscow',
    'uk': 'London',
    'united kingdom': 'London',
    'italy': 'Rome',
    'spain': 'Madrid',
    'saudi arabia': 'Riyadh',
    'turkey': 'Ankara',
    'south africa': 'Pretoria',
    # Add more as needed
}

# A mapping of capital cities to their coordinates (latitude, longitude)
CITY_COORDS = {
    'Cairo': (30.0444, 31.2357),
    'Washington': (38.89511, -77.03637),
    'Paris': (48.8566, 2.3522),
    'Berlin': (52.52, 13.405),
    'Tokyo': (35.6895, 139.6917),
    'Beijing': (39.9042, 116.4074),
    'New Delhi': (28.6139, 77.209),
    'Brasilia': (-15.7939, -47.8828),
    'Ottawa': (45.4215, -75.6996),
    'Canberra': (-35.2809, 149.13),
    'Moscow': (55.7558, 37.6173),
    'London': (51.5074, -0.1278),
    'Rome': (41.9028, 12.4964),
    'Madrid': (40.4168, -3.7038),
    'Riyadh': (24.7136, 46.6753),
    'Ankara': (39.9334, 32.8597),
    'Pretoria': (-25.7479, 28.2293),
    # Add more as needed
}

tf = TimezoneFinder()

def get_timezone(country):
    country = country.strip().lower()
    city = COUNTRY_CAPITALS.get(country)
    if not city:
        return None, None
    coords = CITY_COORDS.get(city)
    if not coords:
        return None, None
    lat, lng = coords
    tz_name = tf.timezone_at(lng=lng, lat=lat)
    return tz_name, city

def get_time_in_country(country):
    tz_name, city = get_timezone(country)
    if not tz_name:
        return f"Sorry, I don't know the time zone for {country.title()}."
    tz = pytz.timezone(tz_name)
    now = datetime.now(tz)
    return f"The current time in {city}, {country.title()} is {now.strftime('%Y-%m-%d %H:%M:%S')} ({tz_name})"

def get_time_difference(country1, country2):
    tz1, city1 = get_timezone(country1)
    tz2, city2 = get_timezone(country2)
    if not tz1 or not tz2:
        return "Sorry, I don't know the time zone for one or both countries."
    now_utc = datetime.utcnow()
    offset1 = pytz.timezone(tz1).utcoffset(now_utc)
    offset2 = pytz.timezone(tz2).utcoffset(now_utc)
    diff = (offset1 - offset2).total_seconds() / 3600
    return f"The time difference between {city1}, {country1.title()} and {city2}, {country2.title()} is {abs(diff)} hours."

def chatbot():
    print("Hello! I can tell you the time in a country or the time difference between two countries.")
    print("Type 'exit' at any prompt to quit.")
    while True:
        print("\nWhat would you like to do?")
        print("1. Get the current time in a country")
        print("2. Get the time difference between two countries")
        choice = input("Enter 1 or 2: ").strip()
        if choice.lower() == 'exit':
            print("Goodbye!")
            break
        if choice == '1':
            country = input("Enter the country name: ").strip()
            if country.lower() == 'exit':
                print("Goodbye!")
                break
            print(get_time_in_country(country))
        elif choice == '2':
            country1 = input("Enter the first country name: ").strip()
            if country1.lower() == 'exit':
                print("Goodbye!")
                break
            country2 = input("Enter the second country name: ").strip()
            if country2.lower() == 'exit':
                print("Goodbye!")
                break
            print(get_time_difference(country1, country2))
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    chatbot()