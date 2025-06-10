import requests

# Your Amadeus credentials
API_KEY = "riYv6e0jaKmRZjYfPdpqzgzv7cDXn3iR"
API_SECRET = "FTSATIbmv4YaGIYr"

# Step 1: Get access token
auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
auth_data = {
    "grant_type": "client_credentials",
    "client_id": API_KEY,
    "client_secret": API_SECRET
}

auth_response = requests.post(auth_url, data=auth_data)

if auth_response.status_code != 200:
    print("❌ Token error:", auth_response.text)
    exit()

access_token = auth_response.json().get("access_token")
print("✅ Access token retrieved")

# Step 2: Use token to get flight offers
headers = {
    "Authorization": f"Bearer {access_token}"
}

search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
params = {
    "originLocationCode": "LHR",
    "destinationLocationCode": "CDG",
    "departureDate": "2025-06-10",
    "adults": 1,
    "nonStop": "false",
    "currencyCode": "USD",
    "max": 3
}

response = requests.get(search_url, headers=headers, params=params)

if response.status_code != 200:
    print("❌ Flight search error:", response.text)
else:
    print("✅ Flight data:")
    print(response.json())
