import requests
from datetime import datetime

API_KEY = "riYv6e0jaKmRZjYfPdpqzgzv7cDXn3iR"
API_SECRET = "FTSATIbmv4YaGIYr"

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }
    res = requests.post(url, data=data)
    return res.json()["access_token"]

def get_flight_details(origin, destination, date):
    token = get_amadeus_token()
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": 1,
        "nonStop": "false",
        "currencyCode": "USD",
        "max": 1
    }
    res = requests.get(url, headers=headers, params=params)
    data = res.json()
    if "data" not in data or not data["data"]:
        return None

    flight = data["data"][0]["itineraries"][0]["segments"][0]

    return {
        "airline": data["data"][0]["validatingAirlineCodes"][0],
        "source_city": origin,
        "destination_city": destination,
        "departure_time": get_part_of_day(flight["departure"]["at"]),
        "arrival_time": get_part_of_day(flight["arrival"]["at"]),
        "stops": "zero" if flight["numberOfStops"] == 0 else "one",
        "duration": convert_duration(data["data"][0]["itineraries"][0]["duration"])
    }

def convert_duration(duration_str):
    # Convert ISO 8601 duration (e.g. PT1H20M) to hours as float
    duration_str = duration_str.replace("PT", "")
    hours = 0
    if "H" in duration_str:
        h = duration_str.split("H")[0]
        hours += int(h)
        duration_str = duration_str.split("H")[1]
    if "M" in duration_str:
        m = duration_str.split("M")[0]
        hours += int(m) / 60
    return round(hours, 2)

def get_part_of_day(iso_datetime):
    hour = datetime.fromisoformat(iso_datetime).hour
    if hour < 6:
        return "Late_Night"
    elif hour < 12:
        return "Morning"
    elif hour < 18:
        return "Afternoon"
    else:
        return "Evening"
