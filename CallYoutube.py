import argparse
from pprint import pprint

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import ProcessInput
from youtube_credentials import DEVELOPER_KEY


class CallYoutube:

    YOUTUBE_URL_PREFIX = "https://www.youtube.com/watch?v="
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    def __init__(self, search_dict: dict):
        self.search_dict = search_dict
        self.artist = search_dict.get("artist", "")
        self.songs = search_dict.get("songs", [])

    def search_youtube(self, artist, song) -> list:
        return_list = []

        youtube = build(
            self.YOUTUBE_API_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            developerKey=DEVELOPER_KEY,
        )

        # Call the search.list method to retrieve results matching the specified query term.
        search_response = (
            youtube.search().list(q=f"{artist} - {song}", part="snippet").execute()
        )
        response_items = search_response.get("items", [])

        for item in response_items:
            if item["id"]["kind"] == "youtube#video":
                # Print the title and video ID of each search result
                title = item["snippet"]["title"]
                video_id = item["id"].get("videoId")
                if video_id:
                    print(f"Title: {title}, Video ID: {video_id}")
                    url = f"{self.YOUTUBE_URL_PREFIX}{video_id}"
                    return_list.append(url)
                    break

        return return_list


test_case = CallYoutube({"artist": "Hozier", "songs": []})
url = test_case.search_youtube("hozier", "jackie and wilson")
print(url)
