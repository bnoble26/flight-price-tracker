import csv

def load_airports(filename):
    with open(filename) as f:
        return [row["code"] for row in csv.DictReader(f)]

uk_airports = load_airports("uk_airports.csv")
destinations = load_airports("popular_destinations.csv")

routes = []

for origin in uk_airports:
    for dest in destinations:
        if origin != dest:
            routes.append({"origin": origin, "destination": dest})

# Save all route pairs
with open("routes.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["origin", "destination"])
    writer.writeheader()
    writer.writerows(routes)

print(f"✅ Generated {len(routes)} routes")
