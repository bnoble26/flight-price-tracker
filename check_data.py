import pandas as pd

df = pd.read_csv("flight_data.csv", parse_dates=["scrape_date", "travel_date"])
print(df.shape)
print(df["travel_date"].min(), "→", df["travel_date"].max())
print(df["origin"].unique(), "→", df["destination"].unique())
