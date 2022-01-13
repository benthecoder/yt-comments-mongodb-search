from urllib.parse import urlparse, parse_qs
from urllib import parse, request
import json
import re


def is_youtube_url(url: str) -> bool:
    """Checks if a string is a youtube url

    Args:
        url (str): youtube url

    Returns:
        bool: true of false
    """

    match = re.match(r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.be)\/.+$", url)
    return bool(match)


def get_vid_id(url: str) -> str:
    """Grabs the video ID of a YouTube URL
    based on two types of YouTube URLs using
    urlparse and parse_qs functions from the
    library urllib.parse

    Args:
        url (str): full YouTube URL

    Returns:
        str: video id of URL
    """
    # for normal YouTube links
    u_parse = urlparse(url)
    # get v key from dictionary output of parse_qs
    id = parse_qs(u_parse.query).get("v")
    # if v query exists:
    if id:
        return id[0]

    # for links obtained through share option in video
    pth = u_parse.path.split("/")
    if pth:
        return pth[-1]


def get_vid_title(video_id: str) -> str:
    """Get the video title of a YouTube video using
    the oembed API

    Args:
        video_id (str): video id of YouTube video

    Returns:
        str: Video title
    """
    params = {"format": "json", "url": f"https://www.youtube.com/watch?v={video_id}"}
    base_url = "https://www.youtube.com/oembed"
    q_str = parse.urlencode(params)
    url = base_url + "?" + q_str

    with request.urlopen(url) as res:
        res_text = res.read()
        data = json.loads(res_text.decode())
        return data["title"]
