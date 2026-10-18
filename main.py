import json

from scraper.royal_caribbean import scrape_cruise
from scraper.google_flights import (
    build_flight_search,
    build_google_flights_url,
    get_flight_price
)

# ---------------------------------
# Cruise URLs to compare
# ---------------------------------

url1 = "https://www.royalcaribbean.com/checkout/summary?groupId=LE08FLL-1526021002&sailDate=2027-03-06&shipCode=LE&packageCode=LE08D143&destinationCode=CARIB&selectedCurrencyCode=USD&country=USA&cabinClassType=INTERIOR&roomIndex=0&r0a=2&r0c=1&r0b=n&r0r=n&r0s=n&r0q=n&r0t=n&r0d=INTERIOR&r0D=y&rgVisited=true&r0C=y&r0e=ZQ&r0L=y&r0f=ZQ&r0g=BESTRATE&r0h=n&r0u=CF056023&r0A=5523.69&r0p=M"
url2 = "https://www.royalcaribbean.com/checkout/summary?groupId=IC07MIA-2623281014&sailDate=2027-03-27&shipCode=IC&packageCode=IC07E484&destinationCode=CARIB&selectedCurrencyCode=USD&country=USA&cabinClassType=INTERIOR&roomIndex=0&r0a=2&r0c=1&r0b=n&r0r=n&r0s=n&r0q=n&r0t=n&r0d=INTERIOR&r0D=y&rgVisited=true&r0C=y&r0e=U5&r0f=U5&r0L=n&r0J=y&r0g=BESTRATE&r0h=n&r0j=9245&r0w=9&r0B=09&r0x=MS&r0y=c534d975-e165-47a0-b3da-00c3093d1844&r0E=%23B80068&r0u=CF056023&r0A=6729.29&r0p=M"

# ---------------------------------
# Scrape cruise information
# ---------------------------------

cruise1 = scrape_cruise(url1)
cruise2 = scrape_cruise(url2)

cruises = [cruise1, cruise2]

print("\nCruise Comparison\n")

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
#save cruise data to json file
with open("data/cruises.json", "w") as file:
    json.dump(
        cruises,
        file,
        default=str,
        indent=4
    )