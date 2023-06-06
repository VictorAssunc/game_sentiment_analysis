import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

nltk.download("vader_lexicon")

# Relation between video and game ids
video_game_ids = {
    "xzCEdSKMkdU": "289650",  # Assassin's Creed Unity
    "d4JnshyKOOQ": "241560",  # The Crew
    "P99qJGrPNLs": "1091500",  # Cyberpunk 2077
    "ASzOzrB-a9E": "1517290",  # Battlefield 2042
    "3DBrG2YjqQA": "271590",  # Grand Theft Auto V
    "O2W0N3uKXmo": "546560",  # Half-Life: Alyx
    "SQEbPn36m1c": "209160",  # Call of Duty: Ghosts
}

# Relation between game ids and game names
game_video_names = {
    "289650": "Assassin's Creed Unity",
    "241560": "The Crew",
    "1091500": "Cyberpunk 2077",
    "1517290": "Battlefield 2042",
    "271590": "Grand Theft Auto V",
    "546560": "Half-Life: Alyx",
    "209160": "Call of Duty: Ghosts",
}

# Load youtube dataset from json file
with open("data/cleaned/youtube_dataset.json") as f:
    youtube_data = json.load(f)

# Load steam dataset from json file
with open("data/cleaned/steam_dataset.json") as f:
    steam_data = json.load(f)

for video_id in youtube_data:
    # Skip video if it is not in the video_game_ids dictionary
    if video_id not in video_game_ids:
        continue

    # Convert comments list to string
    youtube_data[video_id] = [" ".join(comment) for comment in youtube_data[video_id]]
    # Convert reviews list to string
    steam_data[video_game_ids[video_id]] = [
        " ".join(review) for review in steam_data[video_game_ids[video_id]]
    ]

    # Convert comments list to pandas dataframe
    df_youtube = pd.DataFrame(youtube_data[video_id], columns=["comment"])
    # Convert reviews list to pandas dataframe
    df_steam = pd.DataFrame(steam_data[video_game_ids[video_id]], columns=["review"])

    print("\nSentiment analysis for %s" % game_video_names[video_game_ids[video_id]])

    # Sentiment analysis
    sid = SentimentIntensityAnalyzer()
    # Calculate sentiment score for each comment
    df_youtube["sentiment_score"] = df_youtube["comment"].apply(
        lambda x: sid.polarity_scores(x)["compound"]
    )
    # Calculate sentiment score for each review
    df_steam["sentiment_score"] = df_steam["review"].apply(
        lambda x: sid.polarity_scores(x)["compound"]
    )

    # Calculate sentiment score for each video
    video_sentiment_score = df_youtube["sentiment_score"].mean()
    video_sentiment = (
        "positive"
        if video_sentiment_score >= 0.3
        else ("negative" if video_sentiment_score <= -0.3 else "neutral")
    )
    print(
        "Sentiment score from youtube comments for game %s: %s (%f)"
        % (
            game_video_names[video_game_ids[video_id]],
            video_sentiment,
            video_sentiment_score,
        )
    )

    # Calculate sentiment score for each game
    game_sentiment_score = df_steam["sentiment_score"].mean()
    game_sentiment = (
        "positive"
        if game_sentiment_score >= 0.3
        else ("negative" if game_sentiment_score <= -0.3 else "neutral")
    )
    print(
        "Sentiment score from steam reviews for game %s: %s (%f)"
        % (
            game_video_names[video_game_ids[video_id]],
            game_sentiment,
            game_sentiment_score,
        )
    )
