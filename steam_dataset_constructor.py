import json
import requests
import urllib.parse

# Set game IDs
game_ids = [
    "289650",  # Assassin's Creed Unity
    "241560",  # The Crew
    "1091500",  # Cyberpunk 2077
    "1517290",  # Battlefield 2042
    "271590",  # Grand Theft Auto V
    "546560",  # Half-Life: Alyx
    "209160",  # Call of Duty: Ghosts
    # "1971870",  # Mortal Kombat 1 (Not released yet)
    # "588430",  # Fallout Shelter (Free game)
    # "None",  # The Elder Scrolls VI (Not released yet)
    # "None",  # Horizon Forbidden West (Only PlayStation)
    # "None",  # Gran Turismo 7 (Only PlayStation)
]

# Set reference dates for reviews
game_reviews_dates = {
    "289650": {
        "start_date": 1414800000,
        "end_date": 1420077600,
    },
    "241560": {
        "start_date": 1417392000,
        "end_date": 1422756000,
    },
    "1091500": {
        "start_date": 1606780800,
        "end_date": 1612148400,
    },
    "1517290": {
        "start_date": 1635735600,
        "end_date": 1641006000,
    },
    "271590": {
        "start_date": 1427846400,
        "end_date": 1433127600,
    },
    "546560": {
        "start_date": 1583020800,
        "end_date": 1588302000,
    },
    "209160": {
        "start_date": 1383264000,
        "end_date": 1388541600,
    },
}

# Set Steam API URL for reviews of a game
review_url = "https://store.steampowered.com/appreviews/%s?%s"

# Create empty dict for reviews
reviews_by_id = {}

for id in game_ids:
    print("Getting reviews for %s" % id)

    # Create empty list for reviews
    reviews_by_id[id] = []

    # Create count to track number of reviews
    count = 0

    # Set request params
    params = {
        "json": 1,
        "language": "english",
        "filter": "recent",
        "purchase_type": "steam",
        "num_per_page": 100,
        "day_range": 60,
        "start_date": game_reviews_dates[id]["start_date"],
        "end_date": game_reviews_dates[id]["end_date"],
        "date_range_type": "include",
        "cursor": "*",
    }

    # Get reviews
    while True:
        print("\tGetting with cursor %s" % params["cursor"])

        # Get reviews from Steam API
        url = review_url % (id, urllib.parse.urlencode(params))
        response = requests.get(url)
        response_json = response.json()

        # Check if there are no more reviews
        if response_json["query_summary"]["num_reviews"] == 0 or count >= 10000:
            break

        # Iterate over reviews
        for review in response_json["reviews"]:
            # Skip reviews with less than 3 hours of playtime or reviews from free copies
            if (
                review["author"]["playtime_forever"] <= 180
                or review["received_for_free"]
            ):
                continue

            # Save only the review text
            reviews_by_id[id].append(review["review"])

        # Update cursor
        params["cursor"] = response_json["cursor"]

        # Update count
        count += response_json["query_summary"]["num_reviews"]

    print("Got %d reviews" % count)

# Save reviews to file
json_object = json.dumps(reviews_by_id, indent=4)
with open("data/raw/steam_dataset_readable.json", "w") as file:
    file.write(json_object)

with open("data/raw/steam_dataset.json", "w") as file:
    json.dump(reviews_by_id, file)
