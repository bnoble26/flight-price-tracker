import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Load your scraped data
df = pd.read_csv("flight_prices.csv")
df["date_collected"] = pd.to_datetime(df["date_collected"])
df["route"] = df["origin"] + " → " + df["destination"]

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Flight Price Tracker (Live Scraped Data)"),
    
    dcc.Dropdown(
        id="route-dropdown",
        options=[{"label": r, "value": r} for r in sorted(df["route"].unique())],
        value=sorted(df["route"].unique())[0]
    ),
    
    dcc.Graph(id="price-graph")
])

@app.callback(
    dash.dependencies.Output("price-graph", "figure"),
    [dash.dependencies.Input("route-dropdown", "value")]
)
def update_graph(selected_route):
    filtered = df[df["route"] == selected_route]
    fig = px.line(
        filtered,
        x="date_collected",
        y="price_usd",
        title=f"Price over time for {selected_route}",
        markers=True
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
