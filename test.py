from apiclient.discovery import build

api_key = "AIzaSyBKoeIuE-YBM1NYDIEv4chJrRtt_yGq4ic"

youtube = build('youtube', 'v3', developerKey=api_key)

search_response = youtube.search().list(
    part='snippet',
    maxResults=5,
    order="viewCount",
    type="channel",
    fields="items(snippet(channelId, channelTitle))",
    regionCode="kr"
).execute()

print(search_response["items"])