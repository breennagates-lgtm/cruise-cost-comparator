from playwright.sync_api import sync_playwright
from datetime import datetime


def scrape_cruise(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(
            '[data-testid="itinerary-summary-drawer-name"]'
        )




    # find cruise name in the summary drawer
        cruise_name = page.locator(
            '[data-testid="itinerary-summary-drawer-name"]'
        ).first.text_content()


    #find port of departure in the summary drawer
        port = page.locator(
            '[data-testid="itinerary-summary-port"]'
        ).first.text_content()


    #find ship name in the summary drawer
        ship = page.locator(
            '[data-testid="itinerary-summary-ship"]'
        ).first.text_content()


    #find start_date in the summary drawer
        start_date = page.locator(
            '[data-testid="itinerary-summary-start-date"]'
        ).first.text_content()
        #convert to datetime object
        start_date = datetime.strptime(
            start_date,
            "%b %d, %Y"
        ).date()



    #find end date in the summary drawer
        end_date = page.locator(
            '[data-testid="itinerary-summary-end-date"]'
        ).first.text_content()
        #convert to datetime object
        end_date = datetime.strptime(
            end_date,
            "%b %d, %Y"
        ).date()

    #find total price
        pricing = page.locator(
            '.TripTotal_pricingItem__u2hha32'
        ).all_text_contents()

        trip_total_text = pricing[0]

        trip_total = (
            trip_total_text
            .replace("Trip total", "")
            .replace("USD", "")
            .replace("$", "")
            .replace(",", "")
            .strip()
        )

        trip_total = float(trip_total)

        guests = page.locator(
            '[data-testid="rooms-and-guests-link"]'
        ).first.text_content()

        parts = guests.split(",")

        traveler_count = 0

        for part in parts:
            traveler_count += int(
                part.strip().split()[0]
            )


        browser.close()

        return {
            "url": url,
            "cruise_name": cruise_name,
            "port": port,
            "ship": ship,
            "departure_date": start_date,
            "return_date": end_date,
            "trip_total": trip_total,
            "nights": (end_date - start_date).days,
            "guests": guests,
            "traveler_count": traveler_count
        }