from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

app = Flask(__name__)

def load_data():
    file_path = "flight_data.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path, parse_dates=["travel_date", "scrape_date"])
    else:
        return pd.DataFrame(columns=[
            "travel_date", "origin", "destination", "price_gbp",
            "stops", "airline", "duration", "scrape_date"
        ])

@app.route("/", methods=["GET", "POST"])
def index():
    df = load_data()
    if df.empty:
        return render_template("index.html", chart="<p>No data available</p>", 
                               origins=[], destinations=[], stops=[], 
                               origin="", destination="", selected_stops="",
                               last_scrape="N/A", marker="634882")

    # Populate dropdowns
    origins = sorted(df["origin"].unique())
    destinations = sorted(df["destination"].unique())
    stops_options = sorted(df["stops"].dropna().unique())

    # Handle form input
    origin = request.form.get("origin") if request.method == "POST" else origins[0]
    destination = request.form.get("destination") if request.method == "POST" else destinations[0]
    selected_stops = request.form.get("stops")

    # Filter dataset
    filtered = df[(df["origin"] == origin) & (df["destination"] == destination)]
    if selected_stops:
        filtered = filtered[filtered["stops"] == int(selected_stops)]

    if filtered.empty:
        return render_template("index.html", chart="<p>No matching data for selection</p>", 
                               origins=origins, destinations=destinations, 
                               stops=stops_options, origin=origin, 
                               destination=destination, selected_stops=selected_stops, 
                               last_scrape="N/A", marker="634882")

    # Group by date, keep cheapest
    best = filtered.sort_values(by=["travel_date", "price_gbp"]).drop_duplicates(subset=["travel_date"])
    trend = best[["travel_date", "price_gbp", "airline", "duration"]]

    # Plotly chart
    fig = px.line(trend, x="travel_date", y="price_gbp", title=f"Cheapest Fares: {origin} → {destination}",
                  markers=True,
                  hover_data={"airline": True, "duration": True, "price_gbp": True})
    fig.update_traces(mode="markers+lines",
                      hovertemplate="Date: %{x|%Y-%m-%d}<br>Price: £%{y:.2f}<br>Airline: %{customdata[0]}<br>Duration: %{customdata[1]}")
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    chart_html = pio.to_html(fig, full_html=False)

    # Scrape date
    last_scrape = df["scrape_date"].max().strftime("%Y-%m-%d") if not df["scrape_date"].isnull().all() else "N/A"

    return render_template("index.html",
        chart=chart_html,
        origins=origins,
        destinations=destinations,
        stops=stops_options,
        origin=origin,
        destination=destination,
        selected_stops=selected_stops,
        last_scrape=last_scrape,
        marker="634882"
    )

if __name__ == "__main__":
    app.run(debug=True)

