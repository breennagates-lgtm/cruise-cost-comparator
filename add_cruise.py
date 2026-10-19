import json

new_url = input(
    "Paste Royal Caribbean URL: "
).strip()

with open(
    "data/cruise_urls.json",
    "r"
) as f:
    urls = json.load(f)

if new_url in urls:

    print(
        "URL already exists."
    )

else:

    urls.append(new_url)

    with open(
        "data/cruise_urls.json",
        "w"
    ) as f:

        json.dump(
            urls,
            f,
            indent=4
        )

    print(
        "Cruise added successfully."
    )