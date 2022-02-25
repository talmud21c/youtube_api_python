import urllib.request as request
import json

api_key = "AIzaSyBKoeIuE-YBM1NYDIEv4chJrRtt_yGq4ic"

name = input("채널ID를 입력하세요: ")

title_data = request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=snippet&id="+name+"&key="+api_key).read()
title = json.loads(title_data)["items"][0]["snippet"]["title"]

subs_data = request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&id="+name+"&key="+api_key).read()
subs = json.loads(subs_data)["items"][0]["statistics"]["subscriberCount"]


print(title+"채널의 구독자 수는"+subs+"명 입니다.")
