from datetime import date, datetime


def test_night_calculation():
    start = date(2027, 12, 11)
    end = date(2027, 12, 19)

    nights = (end - start).days

    assert nights == 8


def test_date_parsing():
    result = datetime.strptime(
        "Dec 11, 2027",
        "%b %d, %Y"
    ).date()

    assert result.year == 2027
    assert result.month == 12
    assert result.day == 11

def test_price_conversion():
    text = "Trip total$4,553.94 USD"

    result = (
        text
        .replace("Trip total", "")
        .replace("USD", "")
        .replace("$", "")
        .replace(",", "")
        .strip()
    )

    assert float(result) == 4553.94