from datetime import timedelta

from playwright.sync_api import sync_playwright


PORT_TO_AIRPORT = {
    "Fort Lauderdale, Florida": "FLL",
    "Miami, Florida": "MIA"
}


def build_flight_search(
        cruise,
        home_airport="MKE"
):
    arrival_airport = PORT_TO_AIRPORT[
        cruise["port"]
    ]

    departure_date = (
        cruise["departure_date"]
        - timedelta(days=1)
    )

    return_date = cruise["return_date"]

    return {
        "home_airport": home_airport,
        "arrival_airport": arrival_airport,
        "departure_date": departure_date,
        "return_date": return_date
    }


def build_google_flights_url(
        flight_info
):
    return (
        f"https://www.google.com/travel/flights?"
        f"from={flight_info['home_airport']}"
        f"&to={flight_info['arrival_airport']}"
        f"&departure={flight_info['departure_date']}"
        f"&return={flight_info['return_date']}"
    )


def get_flight_price(flight_info):

    home_airport = flight_info["home_airport"]
    arrival_airport = flight_info["arrival_airport"]

    departure_date = str(
        flight_info["departure_date"]
    )

    return_date = str(
        flight_info["return_date"]
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=500
        )

        context = browser.new_context()

        page = context.new_page()

        page.goto(
            "https://www.google.com/travel/flights"
        )

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Origin
        page.get_by_role(
            "combobox",
            name="Where from?"
        ).click()

        page.get_by_role(
            "combobox",
            name="Where else?"
        ).fill(home_airport)

        page.get_by_role(
            "option"
        ).first.wait_for()

        page.get_by_role(
            "option"
        ).first.click()

        # Destination
        page.get_by_role(
            "combobox",
            name="Where to?"
        ).click()

        page.keyboard.type(
            arrival_airport
        )

        page.get_by_role(
            "option"
        ).first.wait_for()

        page.get_by_role(
            "option"
        ).first.click()

        # Open calendar
        page.get_by_role(
            "textbox",
            name="Departure"
        ).click()

        page.locator(
            f'[data-iso="{departure_date}"]'
        ).click()

        page.wait_for_timeout(2000)

        page.locator(
            f'[data-iso="{return_date}"]'
        ).click()

        page.get_by_role(
            "button",
            name="Done"
        ).click()

        page.wait_for_timeout(3000)

        # Search
        page.get_by_role(
            "button",
            name="Search"
        ).click()

        page.wait_for_load_state(
            "networkidle"
        )

        page.wait_for_timeout(5000)

        # Cheapest price
        price_text = page.locator(
            '[aria-label$="US dollars"]'
        ).first.text_content()

        flight_price = int(
            price_text.replace("$", "")
            .replace(",", "")
        )

        context.close()
        browser.close()

        return flight_price