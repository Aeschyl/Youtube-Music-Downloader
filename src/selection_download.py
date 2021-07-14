from pytube import YouTube
import os
import requests
import re

user_request = str.strip(str(input('>> ')))

search_request = user_request + ' song'

youtube_api_key = '<YOUR API KEY HERE>'

snippet_request = requests.get('https://www.googleapis.com/youtube/v3/search', {
                                                                  'part': 'snippet',
                                                                  'q': search_request,
                                                                  'key': youtube_api_key,
                                                                  'maxResults': 3,
                                                                  'type': 'video'})

durations = []

for i in range(0, 3):
    content_details = requests.get('https://www.googleapis.com/youtube/v3/videos', {
                                                                      'part': 'contentDetails',
                                                                      'id': snippet_request.json()['items'][i]['id']['videoId'],
                                                                      'key': youtube_api_key
                                                                      })


    durations.append(content_details.json()['items'][0]['contentDetails']['duration'])

music_options = []

for i in range(0, 3):
    print(str(i + 1) + '.')
    print('Title - ' + snippet_request.json()['items'][i]['snippet']['title'])

    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')

    minutes = minutes_pattern.search(durations[i])
    seconds = seconds_pattern.search(durations[i])

    minutes = minutes.group(1) if minutes else 0
    seconds = seconds.group(1) if seconds else 0

    print('Duration - ' + minutes + ':' + seconds)

    link = 'https://youtube.com/watch?v=' + snippet_request.json()['items'][i]['id']['videoId']
    music_options.append(link)
    print('Link - ' + link)

while True:
        selection = input("\nEnter the index of the music you want: ")
        if selection == '1':
            selected_music = music_options[0]
            break
        elif selection == '2':
            selected_music = music_options[1]
            break
        elif selection == '3':
            selected_music = music_options[2]
            break
        else:
            print("\nSorry, the input was invalid. Please try again with a number like '1'")


yt = YouTube(selected_music)
music = yt.streams.filter(only_audio=True).first()
music_file = music.download()

base, ext = os.path.splitext(music_file)
new_file = base + '.mp3'
os.rename(music_file, new_file)
