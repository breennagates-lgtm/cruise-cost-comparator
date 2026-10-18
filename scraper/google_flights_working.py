from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=500
    )

    context = browser.new_context()

    page = context.new_page()

    page.goto("https://www.google.com/travel/flights")

    # Let Google Flights fully load
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # -------------------------
    # Origin
    # -------------------------

    page.get_by_role("combobox", name="Where from?").click()

    page.get_by_role("combobox", name="Where else?").fill("MKE")

    page.get_by_role("option").first.wait_for()

    page.get_by_role("option").first.click()

    # -------------------------
    # Destination
    # -------------------------

    page.get_by_role("combobox", name="Where to?").click()

    page.keyboard.type("FLL")

    page.get_by_role("option").first.wait_for()

    page.get_by_role("option").first.click()

    # -------------------------
    # Dates
    # -------------------------

    page.get_by_role("textbox", name="Departure").click()

    # Departure
    page.locator('[data-iso="2026-11-17"]').click()

    # Very important:
    # Give Google time to switch to Return mode
    page.wait_for_timeout(2000)

    # Return
    page.locator('[data-iso="2026-11-29"]').click()

    # Close calendar
    page.get_by_role("button", name="Done").click()

    page.wait_for_timeout(3000)

    # -------------------------
    # Search
    # -------------------------

    page.get_by_role("button", name="Search").click()

    page.wait_for_load_state("networkidle")

    page.wait_for_timeout(5000)

    print("PAGE TITLE:")
    print(page.title())

    print("\nCHEAPEST TEXT:")

    try:
        cheapest_text = page.locator("text=Cheapest").first.text_content()
        print(cheapest_text)
    except Exception as e:
        print("Error:", e)

    input("Results loaded. Press Enter to close...")