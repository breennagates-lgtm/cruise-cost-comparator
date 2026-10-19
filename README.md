Cruise Cost Comparator

A Python application that compares Royal Caribbean cruise vacations by combining:

- Cruise fare
- Airfare from your home airport
- Total trip cost
- Cost per night

The tool automatically scrapes cruise information from Royal Caribbean booking URLs, finds flights through Google Flights, and generates an HTML comparison report.

==================================================
FEATURES
==================================================

✓ Scrapes cruise details directly from Royal Caribbean booking URLs
✓ Calculates cruise price, flight price, total vacation cost, and cost per night
✓ Supports multiple cruises
✓ Stores cruise URLs in a JSON configuration file
✓ Automatically sorts cruises by total trip cost
✓ Generates an HTML comparison report
✓ Provides direct links to Royal Caribbean cruise pages and Google Flights
✓ Highlights the cheapest overall option
✓ Filters return flights to departures at 12:00 PM or later
✓ Selects the cheapest qualifying afternoon return flight

==================================================
PROJECT STRUCTURE
==================================================

cruise_cost_comparator/
│
├── main.py
├── add_cruise.py
├── remove_cruise.py
├── cruise_report.html
│
├── data/
│   ├── cruise_urls.json
│   └── cruises.json
│
├── scraper/
│   ├── royal_caribbean.py
│   └── google_flights.py
│
└── .venv/

==================================================
REQUIREMENTS
==================================================

Python 3.11+

Install dependencies:

pip install playwright

Install Playwright browser:

playwright install chromium

==================================================
CONFIGURATION
==================================================

Cruises are stored in:

data/cruise_urls.json

Example:

[
    "https://www.royalcaribbean.com/checkout/summary?...",
    "https://www.royalcaribbean.com/checkout/summary?..."
]

==================================================
ADDING A CRUISE
==================================================

Run:

python add_cruise.py

Paste a Royal Caribbean URL when prompted.

==================================================
REMOVING A CRUISE
==================================================

Run:

python remove_cruise.py

Select the number corresponding to the cruise URL you want removed.

==================================================
GENERATING A COMPARISON REPORT
==================================================

Run:

python main.py

The program will:

1. Load all cruise URLs
2. Scrape cruise details
3. Search Google Flights
4. Calculate airfare
5. Calculate total trip cost
6. Generate an HTML report

==================================================
REPORT INFORMATION
==================================================

- Rank
- Ship
- Cruise
- Departure Date
- Return Date
- Nights
- Cost Per Night
- Cruise Price
- Flight Price
- Total Cost
- Cruise Link
- Flight Link

==================================================
FLIGHT SELECTION RULES
==================================================

1. Searches Google Flights
2. Selects the recommended outbound flight
3. Opens additional return flight options
4. Filters out morning return flights
5. Keeps flights departing at 12:00 PM or later
6. Selects the cheapest qualifying return option
7. Uses the resulting itinerary price for trip calculations

==================================================
OUTPUT FILES
==================================================

data/cruises.json
    Contains scraped cruise information.

cruise_report.html
    Contains the comparison report.

==================================================
CURRENT LIMITATIONS
==================================================

- Designed specifically for Royal Caribbean booking URLs
- Assumes departure airport is configured in the flight scraper
- Depends on Google Flights page structure
- Uses browser automation and may require updates if website layouts change

==================================================
FUTURE ENHANCEMENTS
==================================================

- Save selected flight times
- Display return flight departure times in report
- Savings vs. cheapest cruise column
- Additional cruise lines
- Automatic browser opening improvements
- Cruise history tracking
- Better URL management interface

==================================================
AUTHOR
==================================================

Created by BreEnna Beth Gates as a personal cruise vacation comparison tool for evaluating the true cost of competing cruise options.
