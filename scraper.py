import requests
import pandas as pd
from datetime import datetime, timedelta
import os

# ✈️ Your routes (origin → destination)
ROUTES = [
    ("LHR", "BKK"),
    ("LHR", "DPS"),
    ("LHR", "HAN"),
    ("MAN", "BKK"),
    ("LHR", "MNL")
]

# 🔑 Amadeus sandbox credentials
API_KEY = "riYv6e0jaKmRZjYfPdpqzgzv7cDXn3iR"
API_SECRET = "FTSATIbmv4YaGIYr"

# 🌐 Get access token
def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }
    res = requests.post(url, data=data)
    return res.json()["access_token"]

# 🔍 Query flight prices
def query_route(access_token, origin, destination, date, adults=1):
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": adults,
        "currencyCode": "GBP",
        "max": 3
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        print(f"📦 Fetching {origin} → {destination} on {date}")
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        return res.json().get("data", [])
    except requests.exceptions.Timeout:
        print(f"⏱️ Timeout for {origin} → {destination} on {date}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed for {origin} → {destination} on {date}: {e}")
    return []


# 📦 Save to CSV
def save_to_csv(data, filename="flight_data.csv"):
    df = pd.DataFrame(data)
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

# 🧠 Run for all routes and future dates
def run_scraper():
    token = get_access_token()
    today = datetime.today()
    results = []

    for origin, destination in ROUTES:
        for days_ahead in range(1, 121, 5):  # Sample every 5th day in next 120
            dep_date = (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
            flights = query_route(token, origin, destination, dep_date)
            if not flights:
                continue

            for f in flights:
                itinerary = f["itineraries"][0]["segments"]
                total_duration = f["itineraries"][0]["duration"]
                num_stops = len(itinerary) - 1
                airline = itinerary[0]["carrierCode"]
                price = float(f["price"]["total"])

                results.append({
                    "scrape_date": today.strftime("%Y-%m-%d"),
                    "travel_date": dep_date,
                    "origin": origin,
                    "destination": destination,
                    "price_gbp": price,
                    "stops": num_stops,
                    "airline": airline,
                    "duration": total_duration
                })

    save_to_csv(results)
    print("✅ Scraping complete. Data saved to flight_data.csv")

# 🔁 Run it
if __name__ == "__main__":
    run_scraper()
