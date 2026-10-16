from playwright.sync_api import sync_playwright
from datetime import datetime

url = "https://www.royalcaribbean.com/checkout/summary?groupId=LE08FLL-1526021002&sailDate=2027-12-11&shipCode=LE&packageCode=LE08D169&destinationCode=CARIB&selectedCurrencyCode=USD&country=USA&cabinClassType=INTERIOR&_gl=1*1bwu7mb*_up*MQ..&gclid=41fb2ad8f3f011e2f44c400a7b5a1c19&gclsrc=3p.ds&roomIndex=0&r0a=2&r0c=1&r0b=n&r0r=n&r0s=n&r0q=n&r0t=n&r0d=INTERIOR&r0D=y&rgVisited=true&r0C=y&r0e=ZQ&r0L=y&r0f=ZQ&r0g=BESTRATE&r0h=n&r0m=y&r0A=4553.94&r0p=M"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(5000)

    print(f"URL: {url}")


# find cruise name in the summary drawer
    cruise_name = page.locator(
        '[data-testid="itinerary-summary-drawer-name"]'
    ).first.text_content()
    print(f"Cruise Name: {cruise_name}")

#find port of departure in the summary drawer
    port = page.locator(
        '[data-testid="itinerary-summary-port"]'
    ).first.text_content()
    print(f"Port of departure: {port}")

#find ship name in the summary drawer
    ship = page.locator(
        '[data-testid="itinerary-summary-ship"]'
    ).first.text_content()

    print(f"Ship:  {ship}")

#find start_date in the summary drawer
    start_date = page.locator(
        '[data-testid="itinerary-summary-start-date"]'
    ).first.text_content()
    #convert to datetime object
    start_date = datetime.strptime(
        start_date,
        "%b %d, %Y"
    ).date()

    print(f"Start Date: {start_date}")

#find end date in the summary drawer
    end_date = page.locator(
        '[data-testid="itinerary-summary-end-date"]'
    ).first.text_content()
    #convert to datetime object
    end_date = datetime.strptime(
        end_date,
        "%b %d, %Y"
    ).date()
    print(f"End Date: {end_date}")
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

    print(f"total: ${trip_total}")






