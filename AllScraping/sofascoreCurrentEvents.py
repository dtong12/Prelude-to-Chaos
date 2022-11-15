

import json
import sys
import uuid

import requests
import random

import time
import collections
"""
What I need:
- Get all current games
- Get all current game data
    #Current Set
    #Current points
    #Let's not worry about the game history, we just want full on alarms
"""

#step 1: Get all of the live game data

#and we want to eventually standardize the names


def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def get_softscore_live_games_ids():
    url = "https://api.sofascore.com/api/v1/sport/tennis/events/live"

    payload={}
    headers = {
    'authority': 'api.sofascore.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'max-age=0',
    'if-none-match': 'W/"cdfefab23b"',
    'origin': 'https://www.sofascore.com',
    'referer': 'https://www.sofascore.com/',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    json_response = json.loads(response.text)
    # uprint(json_response)

    # for event in json_response['events']:
    #     print(event['customId'])

    print("Gathering event_ids...")
    event_ids = []
    for event in json_response['events']:
        event_ids.append(event['id'])
    print('Gathered event_ids', event_ids)
    return event_ids


def get_all_game_data(event_id):

    def game_data(event_id):
        url = f"https://api.sofascore.com/api/v1/event/{event_id}"

        payload={}
        headers = {
        'authority': 'api.sofascore.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'max-age=0',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return json.loads(response.text)

    def point_by_point(event_id):

        url = f"https://api.sofascore.com/api/v1/event/{event_id}/point-by-point"
        payload={}
        headers = {
        'authority': 'api.sofascore.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"40af09b3f7"',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return json.loads(response.text)


    def game_statistics(event_id):
        url = f"https://api.sofascore.com/api/v1/event/{event_id}/statistics"

        payload={}
        headers = {
        'authority': 'api.sofascore.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"9fbc230418"',
        'origin': 'https://www.sofascore.com',
        'referer': 'https://www.sofascore.com/',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        #print(event_id, response.status_code)
        return json.loads(response.text)

    return game_data(event_id), point_by_point(event_id), game_statistics(event_id)
    #base_url = f"https://www.sofascore.com/{str(random.randrange(20, 50, 3))}/bwGsVPgc"

def sofascore_main():
    ans = collections.defaultdict(lambda: collections.defaultdict())
    event_ids = get_softscore_live_games_ids()
    print("Gathering all API endpoints...")
    for event_id in event_ids:
        game_data, point_by_point, game_statistics = get_all_game_data(event_id)
        ans[event_id]['url'] = ''
        ans[event_id]['game_data_json'] = game_data
        ans[event_id]['point_by_point'] = point_by_point
        ans[event_id]['game_statistics'] = game_statistics

    with open('softscore_current_event.json', 'w') as f:
        json.dump(ans, f)


if __name__ == "__main__":
    # get_softscore_live_games_ids()
    sofascore_main()

    