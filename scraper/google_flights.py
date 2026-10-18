from datetime import timedelta


PORT_TO_AIRPORT = {
    "Fort Lauderdale, Florida": "FLL",
    "Miami, Florida": "MIA"
}


def build_flight_search(cruise, home_airport="MKE"):
    arrival_airport = PORT_TO_AIRPORT[cruise["port"]]

    departure_date = (
        cruise["departure_date"] - timedelta(days=1)
    )

    return_date = cruise["return_date"]

    return {
        "home_airport": home_airport,
        "arrival_airport": arrival_airport,
        "departure_date": departure_date,
        "return_date": return_date
    }
def build_google_flights_url(flight_info):
    return (
    f"https://www.google.com/travel/flights?"
    f"from={flight_info['home_airport']}"
    f"&to={flight_info['arrival_airport']}"
    f"&departure={flight_info['departure_date']}"
    f"&return={flight_info['return_date']}"
    )


def get_flight_price(
        departure_airport,
        arrival_airport,
        departure_date,
        return_date):
    pass