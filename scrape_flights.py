import requests
import csv
from datetime import datetime, timedelta
# === API KEYS ===
API_KEY = "riYv6e0jaKmRZjYfPdpqzgzv7cDXn3iR"
API_SECRET = "FTSATIbmv4YaGIYr"

# === ROUTE LOADER ===
def load_rotated_routes(filename="routes.csv", chunk_size=3):
    with open(filename, newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        total = len(reader)
        day_index = datetime.today().day % (total // chunk_size + 1)
        start = day_index * chunk_size
        end = start + chunk_size
        return reader[start:end]

ROUTES = load_rotated_routes()

# === FLIGHT DATES TO TRACK ===
# 15 to 120 days ahead
flight_days_out = list(range(30, 46, 5))  # every 3 days for lower API load
flight_dates = [
    (datetime.today() + timedelta(days=offset)).strftime("%Y-%m-%d")
    for offset in flight_days_out
]

# === GET ACCESS TOKEN ===
def get_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")

# === GET FLIGHT PRICE ===
def get_price(token, origin, destination, flight_date):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": flight_date,
        "adults": 1,
        "nonStop": "false",
        "currencyCode": "USD",
        "max": 1
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if "data" not in data or not data["data"]:
        return None
    offer = data["data"][0]
    duration = offer["itineraries"][0]["duration"]
    stops = offer["itineraries"][0]["segments"][0]["numberOfStops"]
    price = float(offer["price"]["total"])
    return {
        "duration": duration,
        "stops": stops,
        "price": price
    }

# === SAVE TO CSV ===
def save_to_csv(row, filename="flight_prices.csv"):
    header = list(row.keys())
    file_exists = False
    try:
        with open(filename, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

# === MAIN SCRAPER ===
def main():
    token = get_token()
    collected_on = datetime.today().strftime("%Y-%m-%d")

    for route in ROUTES:
        for flight_date in flight_dates:
            data = get_price(token, route["origin"], route["destination"], flight_date)
            if data:
                save_to_csv({
                    "date_collected": collected_on,
                    "origin": route["origin"],
                    "destination": route["destination"],
                    "flight_date": flight_date,
                    "class": "Economy",
                    "duration": data["duration"],
                    "stops": data["stops"],
                    "price_usd": data["price"]
                })
                print(f"✔ {route['origin']} → {route['destination']} on {flight_date} saved")
            else:
                print(f"✖ No data for {route['origin']} → {route['destination']} on {flight_date}")

if __name__ == "__main__":
    main()
