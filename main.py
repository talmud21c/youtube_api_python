# 라이브러리 임포트
from googleapiclient.discovery import build
import datetime
import pandas as pd

''' 아래 "<--change here-->" 에 자신의 API-Key를 입력하면 됩니다.
'''


# API key와 YouTube API 버전을 세팅
api_key = "AIzaSyBKoeIuE-YBM1NYDIEv4chJrRtt_yGq4ic"
youtube = build('youtube', 'v3', developerKey=api_key)
print('>>> API key 설정')

# 유튜브 모든 채널에는 'Uploads'라는 기본 채널이 있음
# 해당 채널 ID를 가져온 뒤에, 해당 Uploads의 리스트를 다시 호출해오는 함수

# 유튜브 데이터는 매일 변경됨. 오늘 날짜를 Last_update로 기록하기 위해 Datetime을 사용
today = datetime.datetime.now()
nowDate = today.strftime('%Y-%m-%d')

# 채널id를 가지고 비디오 리스트를 가져오는 함수
def get_channel_videos(channel_id):
    # get Uploads playlist id
    res = youtube.channels().list(id=channel_id, part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    res2 = youtube.channels().list(id=channel_id, part='snippet').execute()
    channel_title = res2['items'][0]['snippet']['title']
    print('>>> 대상 채널명: ' + channel_title)
    videos = []
    next_page_token = None

    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='snippet',
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')

        if next_page_token is None:
            break

    return videos

# 채널의 ID를 입력하면, 그 채널에 속한 비디오를 추출
chan_id = input("채널 아이디: ")
videos = get_channel_videos(chan_id)

print('>>> 대상 채널 ID: '+ chan_id)
print('>>> YouTube에서 해당 채널에 속한 모든 비디오 ID 확인 완료')

# 추출된 비디오 리스트에서 video ID만을 추출하여 list로 만든다.
videoid_list = []
for video in videos:
    id_from_api = video['snippet']['resourceId']['videoId']
    videoid_list.append(id_from_api)

# videoid_list에 ID만 모두 추출하여 저장이 되었다.

# 각 비디오에서 데이터를 추출하여, Dataframe을 만들기 위해 빈 list를 생성한다.
title = []
views = []
likes = []
# 21년 7월 부로 영상에 대한 싫어요 수 제한으로 인해 조회 불가
# dislikes = []
comments = []
upload_date = []
print('>>> 데이터 수집 준비 완료')

# 각 비디오에서 데이터를 가져와서 리스트에 추가한다.
print('>>> 개별 비디오 데이터 수집 시작')
for i in range(len(videoid_list)):
    # for i in range(200):
    request = youtube.videos().list(part='snippet,contentDetails,statistics', id=videoid_list[i])
    response = request.execute()

    if response['items'] == []:
        title.append('-')
        views.append('-')
        likes.append('-')
        # dislikes.append('-')
        comments.append('-')

    else:
        # result에서 추출
        tname = response['items'][0]['snippet']['title']
        vc = response['items'][0]['statistics']['viewCount']
        lc = response['items'][0]['statistics']['likeCount']
        # dlc = response['items'][0]['statistics']['dislikeCount']
        cc = response['items'][0]['statistics']['commentCount']
        pA = response['items'][0]['snippet']['publishedAt']

        # append
        title.append(tname)
        views.append(vc)
        likes.append(lc)
        # dislikes.append(dlc)
        comments.append(cc)
        upload_date.append(pA)

print('>>> 개별 비디오 데이터 수집 완료')
print('>>> 비디오 URL 정리')
# YouTube API 응답에는 Video URL이 없음. 이를 생성하기 위해 prefix + Video ID로 리스트를 만든다.
vidurl_prefix = 'https://www.youtube.com/watch?v='
vidurl_list = []

for i in range(len(videoid_list)):
    vidurl = vidurl_prefix + videoid_list[i]
    vidurl_list.append(vidurl)

# Google API의 응답은 UTC를 기준으로 한다. KST로 변환이 필요하며, KST는 UTC+9이다.

original_pubdate = []
for i in range(len(upload_date)):
    originaldate = upload_date[i]
    convertedtime = datetime.datetime.strptime(originaldate, '%Y-%m-%dT%H:%M:%SZ')
    KSTdate = datetime.datetime.strptime(originaldate, '%Y-%m-%dT%H:%M:%SZ') + datetime.timedelta(hours=9)
    KST_converted = KSTdate.strftime('%Y-%m-%d %H:%M')
    original_pubdate.append(KST_converted)


# 위에까지 생성된 모든 리스트를 하나의 데이터프레임으로 옮긴다.
print('>>> 데이터프레임 형태로 가공')
sum_df = pd.DataFrame([title, original_pubdate, videoid_list, vidurl_list, views, likes, comments]).T

# 편의를 위해 컬럼 이름을 추가해준다.
sum_df.columns = ['title', 'PublishedAt', 'ID', 'URL', 'views', 'likes', 'comments']

# 유튜브 조회수는 매일 다르므로, 오늘 작업 날짜를 데이터프레임으로 추가한다. 시간은 무시한다.
# 데이터 프레임에 넣기 전에, 비디오 개수만큼 날짜가 들어간 리스트를 만든다.
date_list = []
for i in range(len(videoid_list)):
    date_list.append(nowDate)


# 데이터프레임에 'Last_update_Date'을 추가한다.
print('>>> 오늘 날짜(작업일) 기록 중')
sum_df['Last_updated_Date'] = date_list

# 채널명을 다시 가져온다.
res2 = youtube.channels().list(id=chan_id, part='snippet').execute()
channel_title = res2['items'][0]['snippet']['title']

# 오늘 날짜가 들어간 csv 파일을 생성한다.
print('>>> 작업이 완료되었습니다.')
filename = channel_title + '_' + today.strftime('%Y%m%d') + '.csv'
sum_df.to_csv(filename, encoding='utf-8-sig', index=False)
print('결과물: ', filename)
