import requests
import os
import pafy
import re

with open("apikey") as f:
    yt_api_key = f.read()

api_uri = "https://www.googleapis.com/youtube/v3/search?part=snippet&q={}&type=video&key={}"


def get_video_info(query: str, title_append="") -> dict:
    """ 
    Retrives video ID from the youtube API 

    query: Regular ol' search string

    title_append: for appending things to the title of the video
        e.g. If you're using Plex Media Server and trailers must
        be labeled with '-trailer'
    """

    query = query.replace(" ", "+")
    result = requests.get(api_uri.format(query, yt_api_key)).json()

    return result

    # video_id = result["items"][0]["id"]["videoId"]
    # raw_title = result["items"][0]["snippet"]["title"]

    # return {"id" : video_id, "title" : raw_title + title_append}


def get_watch_url(video_id: str) -> str:
    """ Creates watchable / downloadable URL from video's ID """

    return "https://www.youtube.com/watch?v={}".format(video_id)


def download_video(video_url, video_title, directory=os.getcwd()):
    """ Uses pafy to download the video """

    video = pafy.new(video_url)
    hq_video = video.getbest(preftype="mp4")

    # This bit is ugly but it works so ¯\_(ツ)_/¯
    hq_video.download(filepath=directory + video_title +
                      "." + hq_video.extension, quiet=False)
