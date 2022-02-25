from googleapiclient.discovery import build
import pandas as pd
# import seaborn as sns

api_key = 'AIzaSyBKoeIuE-YBM1NYDIEv4chJrRtt_yGq4ic'
channel_id = input("채널ID를 입력해 주세요: ")

youtube = build('youtube', 'v3', developerKey=api_key)

# Function to get channel statistics
def get_channel_stats(youtube, channel_id):

    request = youtube.channels().list(
        part='snippet, statistics',
        id=channel_id
    )
    response = request.execute()
    channel_data = []
    data = dict(
        Channel_title = response["items"][0]['snippet']['title'],
        Channel_subs = response["items"][0]['statistics']['subscriberCount'],
        Views = response["items"][0]['statistics']['viewCount'],
        Total_videos = response["items"][0]['statistics']['videoCount']
    )

    channel_data.append(data)

    return channel_data

print(get_channel_stats(youtube, channel_id))

channel_statistics = get_channel_stats(youtube, channel_id)

channel_data = pd.DataFrame(channel_statistics)

channel_data