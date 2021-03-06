# Youtube Comments Search

This is a streamlit app that allows users to search through the "Never Gonna Give You Up" music video by Rick Astley, or better known as the rickroll video.

## About

The main idea of the app is a filter feature for YouTube video comments. I sometimes do `CMD + F` and look for particular comments and I thought it would be fun to make an app that filters out only comments I'm interested in.

In my app, any user can search for comments in the popular rick roll video. There was restrictions in getting all the comment data however, due to the API quota restrictions. There's also the fact that there are new comments to the video every single day (2,048,385 comments to be exact at the time this markdown was updated)

Nonetheless, I was only able to get ~1 million comments, which I believe is more than enough for this little side project.

To build the web app, I used streamlit because it's easy to use and has tons of features. It has well designed components and I don't have to worry about web dev.

To build the search functionality, I used MongoDB Atlas Search, which was great and simple to set up. I loved the fact that I could test my search index before writing any code. The searches are ranked by the search score of Atlas search by default, so users are getting results that are accurate and matches the query.

This app is hosted on Streamlit Cloud and anyone can have a go at it. [Try it out!](https://share.streamlit.io/benthecoder/yt-comments-mongodb-search/main/yt_comments/app.py)

This project was inspired by the [MongoDB Atlas Hackathon on DEV](https://dev.to/devteam/announcing-the-mongodb-atlas-hackathon-on-dev-4b6m)

## Images of the app

<img src="assets/main.png" width="800" />
<img src="assets/results.png" width="800" /> 
<img src="assets/df-result.png" width="800" />

## Installation

If you want to run this app locally, install [poetry](https://python-poetry.org/) if you don't have it already

### First clone the app 

```bash
  git clone https://github.com/benthecoder/yt-comments-mongodb-search.git
  cd yt-comments-mongodb-search
```

Once you have a mongodb cluster and your YouTube API key ([guide](https://blog.hubspot.com/website/how-to-get-youtube-api-key)) ready. Rename `secrets.toml.example` in the `.streamlit` folder to `secrets.toml` and add your mongodb user name and password, and the API key by replacing them with the YOUR_... phrases. 

### Install dependencies

```bash
  poetry install
```

### Run the streamlit app

```bash
  cd yt_comments
```

```bash
  poetry run streamlit run app.py
```

### Resources

Check your YouTube API quota

- https://console.cloud.google.com/iam-admin/quotas

## Acknowledgement

- [How to Build Your Own Dataset of YouTube Comments | by William Yang | Towards Data Science](https://towardsdatascience.com/how-to-build-your-own-dataset-of-youtube-comments-39a1e57aade)
