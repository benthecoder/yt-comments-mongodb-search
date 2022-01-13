from yt_comments import helper

vid_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
vid_url_short = "https://youtu.be/dQw4w9WgXcQ"
vid_id = "dQw4w9WgXcQ"
vid_title = "Rick Astley - Never Gonna Give You Up (Official Music Video)"


def test_is_youtube_url():
    assert helper.is_youtube_url(vid_url) == True


def test_is_youtube_url_short():
    assert helper.is_youtube_url(vid_url_short) == True


def test_get_vid_id():
    assert helper.get_vid_id(vid_url) == vid_id


def test_get_vid_id_short():
    assert helper.get_vid_id(vid_url_short) == vid_id


def test_get_vid_title():
    assert vid_title == helper.get_vid_title(vid_id)
