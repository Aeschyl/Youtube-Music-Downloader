from pytube import YouTube
import os
import requests
import isodate

search_request = str.strip(str(input('>> ')))

youtube_api_key = '<YOUR API KEY HERE>'

snippet_request = requests.get('https://www.googleapis.com/youtube/v3/search', {
                                                                  'part': 'snippet',
                                                                  'q': search_request,
                                                                  'key': youtube_api_key,
                                                                  'maxResults': 3,
                                                                  'type': 'video'})

durations_in_seconds = []
links_of_videos = []

for i in range(0, 3):
    content_details = requests.get('https://www.googleapis.com/youtube/v3/videos', {
                                                                      'part': 'contentDetails',
                                                                      'id': snippet_request.json()['items'][i]['id']['videoId'],
                                                                      'key': youtube_api_key
                                                                      })

    video_duration = content_details.json()['items'][0]['contentDetails']['duration']
    durations_in_seconds.append(int(isodate.parse_duration(video_duration).total_seconds()))

    link = 'https://youtube.com/watch?v=' + snippet_request.json()['items'][i]['id']['videoId']
    links_of_videos.append(link)

selected_link = ''

if min(durations_in_seconds) == durations_in_seconds[0]:
    selected_link = links_of_videos[0]
elif min(durations_in_seconds) == durations_in_seconds[1]:
    selected_link = links_of_videos[1]
elif min(durations_in_seconds) == durations_in_seconds[2]:
    selected_link = links_of_videos[2]
else:
    print("Some error occurred. Please try again.")


yt = YouTube(selected_link)
music = yt.streams.filter(only_audio=True).first()
music_file = music.download()

base, ext = os.path.splitext(music_file)
new_file = base + '.mp3'
os.rename(music_file, new_file)