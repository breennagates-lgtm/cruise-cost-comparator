import json
from scraper.royal_caribbean import scrape_cruise
from scraper.google_flights import build_flight_search

url1 = "https://www.royalcaribbean.com/checkout/summary?groupId=LE08FLL-1526021002&sailDate=2027-12-11&shipCode=LE&packageCode=LE08D169&destinationCode=CARIB&selectedCurrencyCode=USD&country=USA&cabinClassType=INTERIOR&_gl=1*1bwu7mb*_up*MQ..&gclid=41fb2ad8f3f011e2f44c400a7b5a1c19&gclsrc=3p.ds&roomIndex=0&r0a=2&r0c=1&r0b=n&r0r=n&r0s=n&r0q=n&r0t=n&r0d=INTERIOR&r0D=y&rgVisited=true&r0C=y&r0e=ZQ&r0L=y&r0f=ZQ&r0g=BESTRATE&r0h=n&r0m=y&r0A=4553.94&r0p=M"
url2 = "https://www.royalcaribbean.com/checkout/summary?groupId=HE07MIA-2623280689&sailDate=2027-12-04&shipCode=HE&packageCode=HE07E567&destinationCode=CARIB&selectedCurrencyCode=USD&country=USA&cabinClassType=INTERIOR&roomIndex=0&r0a=2&r0c=1&r0b=n&r0r=n&r0s=n&r0q=n&r0t=n&r0d=OUTSIDE&r0D=y&rgVisited=true&r0C=y&r0e=YQ&r0L=y&r0f=YQ&r0g=BESTRATE&r0h=n&r0m=y&r0A=3868.79&r0p=M"


cruise1 = scrape_cruise(url1)
cruise2 = scrape_cruise(url2)
cruises = [cruise1, cruise2]


flight1 = build_flight_search(cruise1)
flight2 = build_flight_search(cruise2)


print("\nCruise Comparison\n")

for cruise in cruises:
    flight_info = build_flight_search(cruise)
    cost_per_night = cruise["trip_total"] / cruise["nights"]

    print(f"Ship: {cruise['ship']}")
    print(f"Cruise: {cruise['cruise_name']}")
    print(f"Price: ${cruise['trip_total']:.2f}")
    print(f"Nights: {cruise['nights']}")
    print(f"Cost/Night: ${cost_per_night:.2f}")

    print(f"Fly From: {flight_info['home_airport']}")
    print(f"Fly To: {flight_info['arrival_airport']}")
    print(f"Depart: {flight_info['departure_date']}")
    print(f"Return: {flight_info['return_date']}")
    print()

cheapest = min(
    cruises,
    key=lambda c: c["trip_total"]
)

print("Cheapest Cruise:")
print(
    f"{cheapest['ship']} "
    f"at ${cheapest['trip_total']:.2f}"
)

with open("data/cruises.json", "w") as file:
    json.dump(
        cruises,
        file,
        default=str,
        indent=4
    )