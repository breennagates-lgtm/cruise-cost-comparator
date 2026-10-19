import json
import os
from scraper.royal_caribbean import scrape_cruise
from scraper.google_flights import (
    build_flight_search,
    build_google_flights_url,
    get_flight_price
)
# ---------------------------------
# Load cruise URLs from JSON file
# ---------------------------------

with open(
        "data/cruise_urls.json",
        "r"
) as f:
    urls = json.load(f)

cruises = []

for url in urls:
    cruises.append(
        scrape_cruise(url)
    )
print("\nCruise Comparison\n")

results=[]
for cruise in cruises:

    # Build flight search data
    flight_info = build_flight_search(cruise)

    # Get flight price
    flight_price = get_flight_price(
        flight_info
    )

    flight_price = (
            flight_price *
            cruise["traveler_count"]
    )

    # get cost per night
    cost_per_night = (
        cruise["trip_total"] /
        cruise["nights"]
    )
    #find total trip cost
    total_trip_cost = (
        cruise["trip_total"] +
        flight_price
    )

    flight_url = build_google_flights_url(
        flight_info
    )

    results.append({
        "ship": cruise["ship"],
        "cruise": cruise["cruise_name"],
        "nights": cruise["nights"],
        "cruise_price": cruise["trip_total"],
        "flight_price": flight_price,
        "total_cost": total_trip_cost,
        "departure": cruise["departure_date"],
        "return": cruise["return_date"],
        "flight_url": flight_url,
        "cruise_url": cruise["url"],
        "cost_per_night": cost_per_night
    })

    #print to console
    print(f"Ship: {cruise['ship']}")
    print(f"Cruise: {cruise['cruise_name']}")
    print(f"Guests: {cruise['guests']}")
    print(f"Price: ${cruise['trip_total']:.2f}")
    print(f"Nights: {cruise['nights']}")
    print(f"Cost/Night: ${cost_per_night:.2f}")

    print(f"Fly From: {flight_info['home_airport']}")
    print(f"Fly To: {flight_info['arrival_airport']}")
    print(f"Depart: {flight_info['departure_date']}")
    print(f"Return: {flight_info['return_date']}")

    print(
        f"Flight URL: "
        f"{build_google_flights_url(flight_info)}"
    )

    print(f"Flight Price: ${flight_price}")
    print(
        f"Total Trip Cost: "
        f"${total_trip_cost:.2f}"
    )

    print()

# save cruise data to json file
with open("data/cruises.json", "w") as file:
    json.dump(
        cruises,
        file,
        default=str,
        indent=4
    )

# sort cheapest first
results.sort(
    key=lambda x: x["total_cost"]
)

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Cruise Comparison</title>

<style>

body {
    font-family: Arial, sans-serif;
    margin: 30px;
}

h1 {
    color: #003366;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th {
    background: #003366;
    color: white;
    padding: 10px;
}

td {
    padding: 10px;
    border-bottom: 1px solid #ddd;
}

tr:nth-child(even) {
    background-color: #f5f5f5;
}

.best {
    background-color: #c8f7c5 !important;
    font-weight: bold;
}

</style>
</head>

<body>

<h1>Cruise Comparison</h1>

<table>

<tr>
    <th>Rank</th>
    <th>Ship</th>
    <th>Cruise</th>
    <th>Departure</th>
    <th>Return</th>
    <th>Nights</th>
    <th>Cost/Night</th>
    <th>Cruise Price</th>
    <th>Flight Price</th>
    <th>Total Cost</th>
    <th>Cruise</th>
    <th>Flights</th>
</tr>
"""

for index, result in enumerate(results):
    row_class = "best" if index == 0 else ""

    rank = index + 1

    html += f"""
        <tr class="{row_class}">
        <td>{rank}</td>
        <td>{result['ship']}</td>
        <td>{result['cruise']}</td>
        <td>{result['departure']}</td>
        <td>{result['return']}</td>
        <td>{result['nights']}</td>
        <td>${result['cost_per_night']:,.2f}</td>
        <td>${result['cruise_price']:,.2f}</td>
        <td>${result['flight_price']:,.2f}</td>
        <td>${result['total_cost']:,.2f}</td>
        <td>
            <a href="{result['cruise_url']}" target="_blank">
                View Cruise
            </a>
        </td>
        <td>
            <a href="{result['flight_url']}" target="_blank">
                Google Flights
            </a>
        </td>
    </tr>
    """

html += """
</table>

</body>
</html>
"""

with open(
        "cruise_report.html",
        "w",
        encoding="utf-8"
) as f:
    f.write(html)

print("Opening report...")
print(os.path.abspath("cruise_report.html"))
os.startfile("cruise_report.html")
