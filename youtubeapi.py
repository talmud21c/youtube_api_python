from pprint import pprint
from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

# part 파라미터
part_string = 'id, snippet'
# 구독 리스트를 확인할 채널ID
channel_id = 'UCVz6CBSQxCfqdK8hlb30gVQ'


def get_subscription_list(user_id):
    subs = service.subscriptions().list(part='id, snippet', channelId=user_id).execute()
    sub_list = []
    for n in range(subs['pageInfo']['totalResults']):
        channel_list = subs['items'][n]['snippet']['resourceId']['channelId']
        sub_list.append(channel_list)

    return sub_list


print(type(get_subscription_list(channel_id)))
print(get_subscription_list(channel_id))
# 리스트 형태로 출력됨
ch_list = []
for i in range(len(get_subscription_list(channel_id))):
    ch_list.append(get_subscription_list(channel_id)[i])

print(ch_list)


def get_channel_info(ch_id):
    info = service.channels().list(part='id, snippet, statistics', id=ch_id).execute()
    ch_info = [
        info['items'][0]['snippet']['title'],
        info['items'][0]['statistics']['subscriberCount'],
        info['items'][0]['statistics']['viewCount']
    ]

    return ch_info


print(get_channel_info(ch_list[0]))
print(get_channel_info(ch_list[1]))
print(get_channel_info(ch_list[2]))
print(get_channel_info(ch_list[3]))



# # response를 딕셔너리 형태로 반환
# subscribe_list = service.subscriptions().list(
#     part=part_string,
#     channelId=channel_id,
# ).execute()
# print(type(subscribe_list))
# pprint(subscribe_list)
# print()
#
#
# CH_ID = []
# # 채널 갯수만큼 반복 실행
# for n in range(subscribe_list['pageInfo']['totalResults']):
#     data = dict(
#         Channel_title=subscribe_list['items'][n]['snippet']['title'],
#         Channel_id=subscribe_list['items'][n]['snippet']['resourceId']['channelId']
#     )
#     CH_ID.append(data)
#
# print(type(CH_ID))
# pprint(CH_ID)
# print()
#
#
# for i in range(len(CH_ID)):
#     sub_list = CH_ID[i]['Channel_id']
#
#     channel_info = service.channels().list(
#         part='id, snippet, statistics',
#         id=sub_list
#     ).execute()
#
#     # 딕셔너리 한개씩 출력 확인
#     print(type(channel_info))
#     pprint(channel_info)
#     print('---------------------------------------')
#     # 각각의 딕셔너리를 합쳐야됨
#
# for n in range(len(CH_ID)):
#     CH_INFO = []
#     CH_DATA = dict(
#         CH_TITLE=channel_info['items'][0]['snippet']['localized']['title'],
#         CH_SUBS=channel_info['items'][0]['statistics']['subscriberCount'],
#         CH_VIEWS=channel_info['items'][0]['statistics']['viewCount']
#     )
#     CH_INFO.append(CH_DATA)
#
#     print(type(CH_DATA))
#     pprint(CH_DATA)
#     print()
