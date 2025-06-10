import pandas as pd

df = pd.read_csv("flight_data.csv", parse_dates=["travel_date"])
route_counts = df.groupby(["origin", "destination"]).size()
print(route_counts)
