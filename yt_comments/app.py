from functools import wraps
import time
import streamlit as st
import pymongo
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

import pandas as pd
import re

from helper import get_vid_id, get_vid_title, is_youtube_url
from yt_ops import build_service, get_data

DB_USER = st.secrets["mongo"]["DB_USER"]
DB_PASSWORD = st.secrets["mongo"]["DB_PASSWORD"]
VID_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # rickroll video url

st.set_page_config(page_title="YT Comments", page_icon="🔍")


def connect_mongodb():
    CONN_URI = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@youtube.oxcks.mongodb.net/youtube?retryWrites=true&w=majority"
    client = MongoClient(CONN_URI)

    return client


def local_css(file_name):
    with open(file_name) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


def query_mongodb(db, query: str):
    # if sort_by == "Search Score":
    #     sort = "highlights[0].score"
    # elif sort_by == "Number of Likes":
    #     sort = "like_count"
    # else:
    #     sort = "reply_count"

    cursor = db.comments.aggregate(
        [
            {
                "$search": {
                    "index": "test-index",  # text index created to map String data type
                    # https://docs.atlas.mongodb.com/atlas-search/text/
                    "text": {
                        "query": query,
                        "path": "comment",
                    },
                    "highlight": {"path": "comment"},
                }
            },
            {"$addFields": {"highlights": {"$meta": "searchHighlights"}}},
            # {"$sort": {sort: -1}}, # memory issues, can be solved with allowDiskUse
            # {"allowDiskUse": True}, # only available on dedicated cluster
            {
                "$project": {
                    "_id": 0,
                    "comment": 1,
                    "like_count": 1,
                    "reply_count": 1,
                    "score": {"$meta": "searchScore"},
                }
            },
        ]
    )

    return cursor


def main():

    st.title("YouTube Comments Search 🔍")
    st.subheader("Search for anything in the a video's comments!")

    # css style for highlighting text
    local_css("./style.css")

    vid_id = get_vid_id(VID_URL)

    st.caption("Currently working for Rick Astley's rick roll video only")
    st.subheader(get_vid_title(vid_id))
    st.video(VID_URL)

    client = connect_mongodb()
    db = client.videos

    document_cnt = db.comments.count_documents({})

    ## run this to get the comments data
    # get_data(vid_id, db, initial_call = True)
    ## run this to add more comments data to existing collection
    # get_data(vid_id, db, initial_call = False)

    query = st.text_input(
        f"Search out of {document_cnt} comments (Note: the more common the word the longer it will take)",
        "rickrolled",
    )
    top_match_n = st.slider("Select top results", 0, 100, 25)
    # sort_by = st.radio(
    #     "Select sort by", ["Search Score", "Number of Likes", "Number of Replies"]
    # )
    if query == "":
        st.warning("Please enter a query")
    else:
        cursor = query_mongodb(db, query)
        res_list = list(cursor)
        count = len(res_list)

        if count == 0:
            st.write("No comments matching that query... Do another search please")
            st.markdown(
                "![Not found gif](https://media.giphy.com/media/6uGhT1O4sxpi8/giphy.gif)"
            )
        else:
            st.success(f"Done! Showing top {top_match_n} match(es) out of {count}!")
            for item in res_list[:top_match_n]:
                comment = item.get("comment")
                author_name = item.get("authorName")

                pattern = re.compile(query, re.IGNORECASE)
                comment = pattern.sub(
                    f"<span class='highlight bold green'> {query} </span>",
                    comment,
                )

                t = f"<ul><li>{comment} <span class='highlight user'> {author_name} </span></li><ul>"

                st.markdown(t, unsafe_allow_html=True)

        # data frame for results
        df = pd.DataFrame(res_list)
        if "highlights" in df.columns:
            df["score"] = df["highlights"].apply(
                lambda x: re.sub("[^\d\.]", "", str(x))
            )
            df.drop("highlights", axis=1)
        st.subheader("All matching comments below")
        st.dataframe(df)

        # # raw data form
        # st.subheader("Raw comments data")
        # st.json(res_list)


if __name__ == "__main__":
    main()
