import time
import requests
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv

import socket

#事前に取得したYouTube API key
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

YT_API_KEY = os.environ.get("YOUTUBE_API")

HOST = '127.0.0.1'
PORT = 50007


def get_chat_id(yt_url):
    '''
    https://developers.google.com/youtube/v3/docs/videos/list?hl=ja
    '''
    video_id = yt_url.replace('https://www.youtube.com/watch?v=', '')
    print('video_id : ', video_id)

    url    = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'key': YT_API_KEY, 'id': video_id, 'part': 'liveStreamingDetails'}
    data   = requests.get(url, params=params).json()
    
    liveStreamingDetails = data['items'][0]['liveStreamingDetails']
    if 'activeLiveChatId' in liveStreamingDetails.keys():
        chat_id = liveStreamingDetails['activeLiveChatId']
        print('get_chat_id done!')
    else:
        chat_id = None
        print('NOT live')

    return chat_id




def get_chat(chat_id, pageToken):
    '''
    https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list
    '''
    url    = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
    params = {'key': YT_API_KEY, 'liveChatId': chat_id, 'part': 'id,snippet,authorDetails'}

    #チャットの差分を取得するためのトークン
    if type(pageToken) == str:
        params['pageToken'] = pageToken

    data   = requests.get(url, params=params).json()
    
    msgs = []
    try:
        for item in data['items']:
            data_format = {
                "user" : "",
                "msg":"",
                "isSuper":False,
                "superAmount":"",
                "superMsg":"",
                "isOwner":False
            }
            channelId = item['snippet']['authorChannelId']
            msg       = item['snippet']['displayMessage']
            usr       = item['authorDetails']['displayName']
            isOwner   = item['authorDetails']['isChatOwner']
            if 'superChatDetails' in item['snippet']:
                data_format['isSuper'] = True
                data_format['superAmount'] = item['snippet']['superChatDetails']['amountDisplayString']
                data_format['superMsg'] = item['snippet']['superChatDetails']['userComment']
            else:
                isSuper = False
                supAmount = "0"
                supMsg = ""
            log_text  = '[by {}  https://www.youtube.com/channel/{}]\n  {}'.format(usr, channelId, msg)
            print(log_text)

            data_format['user'] = usr
            data_format['msg'] = msg
            data_format['isOwner'] = isOwner
            print(data_format) 
            msgs.append(data_format.copy())
            # print(msgs)
            # with open(log_file, 'a') as f:
            #     print(log_text, file=f)
            #     print(log_text)
        print('start : ', data['items'][0]['snippet']['publishedAt'])
        print('end   : ', data['items'][-1]['snippet']['publishedAt'])

    except Exception as e:
        print(e)
        pass
    return data['nextPageToken'], msgs

def send_message(msgs, client):
    for msg in msgs:
        json_text = json.dumps(msg,ensure_ascii=False)
        client.sendto(json_text.encode('utf-8'), (HOST, PORT))


def main(yt_url):
    slp_time        = 1 #sec
    iter_times      = 90 #回
    take_time       = slp_time / 60 * iter_times
    print('{}分後　終了予定'.format(take_time))
    print('work on {}'.format(yt_url))

    # log_file = yt_url.replace('https://www.youtube.com/watch?v=', '') + '.txt'
    # with open(log_file, 'a') as f:
    #     print('{} のチャット欄を記録します。'.format(yt_url), file=f)
    try:
        chat_id  = get_chat_id(yt_url)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    except Exception as e:
        print(e)
    
    
    nextPageToken = None
    for ii in range(iter_times):
        #for jj in [0]:
        try:
            print('\n')
            nextPageToken, msgs= get_chat(chat_id, nextPageToken)
            send_message(msgs, client)
            time.sleep(slp_time)
        except Exception as e:
            print(e)
            break




if __name__ == '__main__':
    yt_url = input('Input YouTube URL > ')
    main(yt_url)
