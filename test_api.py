import requests
import json

url = "https://kiwi-com-cheap-flights.p.rapidapi.com/round-trip"

querystring = {
    "source": "LHR",
    "destination": "CDG",
    "outbound": "2025-06-10",
    "return": "2025-06-15",
    "currency": "usd",
    "locale": "en",
    "adults": "1",
    "children": "0",
    "infants": "0",
    "cabinClass": "ECONOMY",
    "sortBy": "QUALITY",
    "sortOrder": "ASCENDING",
    "transportTypes": "FLIGHT",
    "limit": "3"
}

headers = {
    "X-RapidAPI-Key": "e1077ba494msh9e5a71ca06ccea5p1d3c89jsn2a4d4a698d5e",
    "X-RapidAPI-Host": "kiwi-com-cheap-flights.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

try:
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print("❌ Failed to parse JSON:", e)
    print("Raw response:")
    print(response.text)

