from apiclient.discovery import build
import streamlit as st

API_KEY = st.secrets["youtube"]["API_KEY"]

# build service for calling YouTube API
def build_service():
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)


# get data from API
def get_data(vid_id: str, db, initial_call=True):
    service = build_service()

    latest_res = db.pageTokens.aggregate(
        [{"$addFields": {"lastElem": {"$last": "$pageTokens"}}}]
    )

    lastest_token = list(latest_res)[0].get("lastElem")

    # first call for data
    if initial_call:
        response = (
            service.commentThreads()
            .list(
                part="snippet",  # replies will return replies to comment
                maxResults=100,  # max is 100
                textFormat="plainText",
                order="time",  # other option is relevance
                videoId=vid_id,
            )
            .execute()
        )

        # insert first page token to collection
        db.pageTokens.insert_one(
            {"_id": vid_id, "pageTokens": [response["nextPageToken"]]}
        )
    else:
        response = (
            service.commentThreads()
            .list(
                part="snippet",  # replies will return replies to comment
                maxResults=100,  # max is 100
                textFormat="plainText",
                order="time",  # other option is relevance
                videoId=vid_id,
                pageToken=lastest_token,
            )
            .execute()
        )

    # loop will continue until quota is maxed
    page = 0
    while response:

        print(f"page {page}")
        page += 1
        index = 0

        data_list = []

        for item in response["items"]:

            print(f"comment {index}")
            index += 1

            top_level_comment = item["snippet"]["topLevelComment"]
            comment_id = top_level_comment["id"]
            comment = top_level_comment["snippet"]["textDisplay"]
            like_count = top_level_comment["snippet"]["likeCount"]
            author_name = top_level_comment["snippet"]["authorDisplayName"]
            date_published = top_level_comment["snippet"]["publishedAt"]
            date_updated = top_level_comment["snippet"]["updatedAt"]
            reply_count = item["snippet"]["totalReplyCount"]

            # insert into mongodb database
            data_list.append(
                {
                    "_id": comment_id,
                    "comment": comment,
                    "reply_count": reply_count,
                    "like_count": like_count,
                    "authorName": author_name,
                    "datePublished": date_published,
                    "dateUpdated": date_updated,
                }
            )

        # ordered=False allows inserts to skips duplicates
        db.comments.insert_many(data_list, ordered=False)

        try:
            if "nextPageToken" in response:
                response = (
                    service.commentThreads()
                    .list(
                        part="snippet",
                        maxResults=100,
                        textFormat="plainText",
                        order="time",
                        videoId=vid_id,
                        pageToken=response["nextPageToken"],
                    )
                    .execute()
                )
                # add pageToken to collection
                db.pageTokens.update_one(
                    {"_id": vid_id},
                    {"$push": {"pageTokens": response["nextPageToken"]}},
                )
            else:
                break
        except Exception as e:
            st.exception(e)
            break
