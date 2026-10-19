import json

with open(
    "data/cruise_urls.json",
    "r"
) as f:
    urls = json.load(f)

if not urls:
    print("No cruises found.")
    exit()

print("\nSaved Cruise URLs:\n")

for index, url in enumerate(urls, start=1):
    print(f"{index}. {url}")

choice = int(
    input(
        "\nEnter number to remove: "
    )
)

if 1 <= choice <= len(urls):

    removed = urls.pop(choice - 1)

    with open(
        "data/cruise_urls.json",
        "w"
    ) as f:

        json.dump(
            urls,
            f,
            indent=4
        )

    print("\nRemoved:")
    print(removed)

else:

    print("Invalid selection.")