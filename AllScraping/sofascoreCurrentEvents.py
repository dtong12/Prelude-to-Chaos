

import json
import sys
import uuid

import requests
import random

import time
import collections

import aiohttp
import asyncio
import platform
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
    print('Finished gathering event_ids', event_ids)
    print(f"Found {len(event_ids)} events")
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
        print("game data", response.status_code)
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
        print("point by point", response.status_code)
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
        print('game statistics', response.status_code)
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


# def test_async_within_sync():
#     main_2()
ans = collections.defaultdict(lambda: collections.defaultdict())


async def async_game_data(session, event_id):
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

        async with session.get(url, headers=headers, data=payload) as response:
            # response = requests.request("GET", url, headers=headers, data=payload)
            # print("game data", response.status)
            response_res = await response.json(content_type=None)
            ans[event_id]['game_data_json'] = response_res


async def async_point_by_point(session, event_id):

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
    async with session.get(url, headers=headers, data=payload) as response:
        #response = requests.request("GET", url, headers=headers, data=payload)
        # print("point by point", response.status)
        response_res = await response.json(content_type=None)
        ans[event_id]['point_by_point'] = response_res


async def async_game_statistics(session, event_id):
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
    async with session.get(url, headers=headers, data=payload) as response:
        response_res = await response.json(content_type=None)
        ans[event_id]['game_statistics'] = response_res


if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
def async_sofascore_main():
    
    start_time = time.time()
    all_event_ids = get_softscore_live_games_ids()
    print("all event ids", all_event_ids)

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for event_id in all_event_ids:
                tasks.append(asyncio.ensure_future(async_game_data(session, event_id)))
                tasks.append(asyncio.ensure_future(async_point_by_point(session, event_id)))
                tasks.append(asyncio.ensure_future(async_game_statistics(session, event_id)))
            asyncio_gather = await asyncio.gather(*tasks)

    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))
    print("length of res", len(ans))

    with open('softscore_current_event.json', 'w') as f:
        json.dump(ans, f)

    file1 = open("myfile.txt", "w")  # write mode
    file1.write("RUN \n")
    file1.close()


if __name__ == "__main__":
    # sofascore_main()
    # test_async_within_sync()
    # main_2()
    #print("running main")
    async_sofascore_main()


    