import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

youtube_url = "https://www.youtube.com/watch?v=%s"
video_ids = [
    "UZ6eFEjFfJ0",  # Mortal Kombat 1
    "xzCEdSKMkdU",  # Assassin's Creed Unity
    "d4JnshyKOOQ",  # The Crew
    "P99qJGrPNLs",  # Cyberpunk 2077
    "ASzOzrB-a9E",  # Battlefield 2042
    "HY4jCjufLG8",  # Fallout Shelter
    "OkFdqqyI8y4",  # The Elder Scrolls VI
    "3DBrG2YjqQA",  # Grand Theft Auto V
    "O2W0N3uKXmo",  # Half-Life: Alyx
    "Lq594XmpPBg",  # Horizon Forbidden West
    "SQEbPn36m1c",  # Call of Duty: Ghosts
    "oz-O74SmTSQ",  # Gran Turismo 7
]

comments_url = "https://hadzy.com/api/comments/%s?page=%d&size=100&sortBy=publishedAt&direction=asc&searchTerms=&author="

comments_by_id = {}

for id in video_ids:
    page, max_pages, count = 0, 0, 0
    stop_date, last_date = None, None
    comments_by_id[id] = []

    print("Getting comments for %s" % id)

    while True:
        if (stop_date is not None and last_date is not None) and stop_date <= last_date:
            break

        if count >= 10000:
            break

        if max_pages != 0 and page >= max_pages:
            break

        print("\tGetting page %d" % page)
        response = requests.get(comments_url % (id, page))
        if response.status_code != 200:
            break

        comments = response.json()["content"]
        if page == 0:
            max_pages = response.json()["pageInfo"]["totalPages"]
            first = comments[0]["publishedAt"]
            stop_date = datetime.strptime(first, "%Y-%m-%dT%H:%M:%S") + relativedelta(
                months=1
            )

        for comment in comments:
            comments_by_id[id].append(comment["textDisplay"])

        last = comments[-1]["publishedAt"]
        last_date = datetime.strptime(last, "%Y-%m-%dT%H:%M:%S")

        page += 1
        count += len(comments)

    print("Got %d comments" % count)

json_object = json.dumps(comments_by_id, indent=4)
with open("data/raw/youtube_dataset_readable.json", "w") as file:
    file.write(json_object)

with open("data/raw/youtube_dataset.json", "w") as file:
    json.dump(comments_by_id, file)
