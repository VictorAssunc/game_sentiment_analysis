import html
import json
import langdetect
import nltk
import nltk.corpus
import nltk.tokenize
import re
import sys

# Download nltk resources
nltk.download("stopwords")
nltk.download("punkt")

# Load stopwords
stop_words = set(nltk.corpus.stopwords.words("english"))


def clean_dataset(name):
    # Loads dataset from json file
    with open("data/raw/" + name + ".json") as f:
        data = json.load(f)

    cleaned_data = {}

    for k, v in data.items():
        cleaned_data[k] = []

        for i in v:
            text = i
            # Ignore text shorter than 3 words
            if len(text.split()) < 3:
                continue

            # HTML unescape
            text = html.unescape(text)

            # Encode text to UTF-8
            text = text.encode("utf-8", errors="ignore").decode()

            # Lowercase text
            text = text.lower()

            # Remove HTML tags
            text = re.sub(r"<[^>]+>", " ", text)

            # Remove URLs, mentions, hashtags, emojis, punctuation, etc.
            text = re.sub(
                r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|http.+?|\d+",
                " ",
                text,
            )

            # Remove extra whitespaces
            text = re.sub(r"\s+", " ", text)

            # Ignore text shorter than 3 words after cleaning
            if len(text.split()) < 3:
                continue

            # Removes non-English tweets
            if langdetect.detect(text) == "en":
                # Tokenize text
                token = nltk.tokenize.word_tokenize(text)

                # Remove stopwords
                text = [w for w in token if not w in stop_words]

                # Remove words with length less than 2
                text = [w for w in text if len(w) > 2]

                # Ignore text shorter than 3 words after removing stopwords
                if len(text) < 3:
                    continue

                # Save cleaned text
                cleaned_data[k].append(text)

    # Save cleaned dataset to file
    json_object = json.dumps(cleaned_data, indent=4)
    with open(("data/cleaned/%s_readable.json" % name), "w") as file:
        file.write(json_object)

    with open(("data/cleaned/%s.json" % name), "w") as file:
        json.dump(cleaned_data, file)


dataset = sys.argv[1]
file = ""
if dataset == "steam":
    file = "steam_dataset"
elif dataset == "youtube":
    file = "youtube_dataset"
else:
    print("Invalid dataset name")
    exit()

clean_dataset(file)
