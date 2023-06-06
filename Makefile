run:
	python main.py

youtube_dataset:
	python youtube_dataset_constructor.py

steam_dataset:
	python steam_dataset_constructor.py

datasets: youtube_dataset steam_dataset

clean_youtube:
	python clean_dataset.py youtube

clean_steam:
	python clean_dataset.py steam

clean_datasets: clean_youtube clean_steam

sentiment:
	python sentiment_analysis.py