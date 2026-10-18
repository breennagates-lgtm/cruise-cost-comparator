import re
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

        try:

            page.goto(
                "https://www.google.com/travel/flights"
            )

            page.wait_for_load_state(
                "networkidle"
            )

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

            # Dates
            page.get_by_role(
                "textbox",
                name="Departure"
            ).click()

            page.locator(
                f'[data-iso="{departure_date}"]'
            ).click()

            page.wait_for_timeout(1000)

            page.locator(
                f'[data-iso="{return_date}"]'
            ).click()

            page.get_by_role(
                "button",
                name="Done"
            ).click()

            page.wait_for_timeout(2000)

            # Search
            page.get_by_role(
                "button",
                name="Search"
            ).click()

            page.wait_for_load_state(
                "networkidle"
            )

            page.wait_for_timeout(5000)

            cards = page.locator(
                ".OgQvJf"
            )

            #print(
            #   "Cards found:",
            #  cards.count()
            #)

            if cards.count() == 0:
                print(
                    "No flight cards found"
                )
                return 0

            # FIRST FLIGHT RESULT

            cards.first.click()

            page.wait_for_timeout(3000)

            #print(
            #    "Clicked first card"
            #)

            # OPEN FULL RETURN FLIGHT LIST

            view_more = page.get_by_text(
                "View more flights",
                exact=True
            )

            if view_more.count() > 0:

                view_more.click()

                page.wait_for_timeout(3000)

                #print(
                #    "Clicked View more flights"
                #)

            else:

                print(
                    "View more flights not found"
                )
            # FIND CHEAPEST RETURN FLIGHT DEPARTING AT OR AFTER NOON


            body_text = page.locator(
                "body"
            ).text_content()

            start = body_text.find(
                "Top returning flights"
            )

            if start >= 0:
                text = body_text[start:start + 15000]
            else:
                text = body_text

            text = text.replace(" ", " ")

            matches = re.findall(
                r'(\d{1,2}:\d{2}\s*[AP]M).*?\$(\d[\d,]*)',
                text,
                re.DOTALL
            )

            candidates = []

            seen = set()

            for time_str, price_str in matches:

                key = (time_str, price_str)

                if key in seen:
                    continue

                seen.add(key)

                # Only PM flights
                if "PM" not in time_str:
                    continue

                price = int(
                    price_str.replace(",", "")
                )

                candidates.append(
                    (
                        price,
                        time_str
                    )
                )

            #print(
            #    "PM candidates:",
            #   candidates
            #)

            if not candidates:
                print(
                    "No afternoon flights found"
                )

                return 0

            cheapest_price, cheapest_time = min(
                candidates,
                key=lambda x: x[0]
            )

            #print(
            #   f"Selected return flight: "
            #   f"{cheapest_time} "
            #    f"${cheapest_price}"
            #)

            return cheapest_price

    #exception block
        except Exception as e:

            print(
                "Google Flights error:"
            )

            print(e)

            return 0

        finally:

            context.close()
            browser.close()