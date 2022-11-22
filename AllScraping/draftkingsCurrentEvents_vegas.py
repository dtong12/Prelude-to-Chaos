import requests
import collections
import json
from datetime import datetime
import pytz
import time

import aiohttp
import asyncio
import platform


region_tag = 'va'

payload = {}
headers = {
    'authority': f'sportsbook-us-{region_tag}.draftkings.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'origin': 'https://sportsbook.draftkings.com',
    'referer': 'https://sportsbook.draftkings.com/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'Cookie': 'STE="2022-11-18T04:07:01.1274914Z"; STH=31feec107a5f8c83ca8b56faf257fad5e43a8ea2d32985684891c2c9583d9fff; STIDN=eyJDIjoxMjIzNTQ4NTIzLCJTIjo0MDYyMzk0MTYwMywiU1MiOjQyNzg3ODY0MzQ0LCJWIjoyMDM5MzY3NjczNSwiTCI6MSwiRSI6IjIwMjItMTEtMThUMDQ6MDY6NTUuODA5MDAyOVoiLCJTRSI6IlVTLURLIiwiVUEiOiJ6bHN6dWhMZW8wZlpOZ2c2djZwYlAwaHpiUDVrMEFTMC9td0k2VGxsa2hZPSIsIkRLIjoiY2FkN2RkNGUtMzQ1NS00N2YwLTkwNGUtZDJkZjJmN2I1OTExIiwiREkiOiIwMzEwMTE1Ni1jZjk1LTQ5N2YtYjBiMi0zMWQ5NWUzMTAyYzAiLCJERCI6MjE3NjQ2NzcxMzJ9; _abck=08C127B41C6047E3A38AF5AC0AF6F2B5~-1~YAAQtvkwF/JL+3uEAQAAUJbPiAhdU6W9KaZiPuoxpFusNYicKASYdmLRl3VTPOofa4W+e6hypZpNbOWeBwxPmi096LiO4u4khbTBufOMaq/Oulu2TCaP6SufVuYEcV8R9dxvaBrPa1P0UoJ8/FZQBluESnyYzXdKJD2b0yAvqYm4jXVO8/chIxQTgwE97tg30K05dgkKN94/i1t2FhlVVRB8WQyB0XzuWRVSMfwjdowBfFBNs7yPS5Y7PA7UkmhaOISjE4XFKFYrH1ARMkxjmuzNDgHG3reTUnMTEEGDD3ZTId5iFN0CuUeM/zQ9xjB+enCheBrKiE8jZP0XuaiOreUwG7FNMRRzegk8Zgutt7ID55LK0SEfdU9zdcZ4QFZiiEhP2H1AD2f56EI7dyHIrdfpc7IGsl70Ib7Fh8Q=~-1~-1~-1; _csrf=20c6fe40-0c53-41b5-8ed8-6c2b6df85b76; ak_bmsc=F68EAF36D7F1A970F5342E8896E330D2~000000000000000000000000000000~YAAQtvkwF/NL+3uEAQAAUJbPiBEsST8LAZQM9LJJ94z0tPO3JKwPLbIaAPMmGl8TZjWuoG+mVscEShar458YfwWJz3eJLE/FwvvVs34NvFlqQF9qGXD/Iw0LNN2nU79IPEkKF+eWfuESCrVT0hq7SYj/+zDD9vy5BZ4xRVT4a0woXdQ4cj1id5LJxr2FoXXPqaBGo6aaLEC4/DdrgliWutvfkSc+9iMyTzfkWZmDsrFB9oOJc79InPrcuuoAuVksxIj9uqwoEYe7/8Sh6SyD6coTX2U0CVNhg9dmGog0pmq4TaMcsUHdqyJo8tMEJTm3+SpSD/hPXPGr03T2FMcXxObqTzw30IvQepy5ThOnX+Hbx0W77f2O0eVx6mId4MY=; bm_sv=7E4A36C18506DABAF3953F5CE22F775B~YAAQtvkwF0tM+3uEAQAAFqzPiBF6F0iQK7zRhgj1SPdiMBC2FYaDVgMguyRTgz7vZ1BpkAtFuTzO5LJ/h0c1Ue14ualbo4A+tFMce1SCijEZkBb7b6kowRSzZ/SgOYwdrMdo8rzHV7+yygHoEccLFbUNM6tU4HEsdh2J7tfBdmZ+gBsfSPbeIJFvu0iV6JBO3si81zujEKXbRftZ7diMNItllmqlDCy/x/6cDDC6xXN3i/ggb9TOnpsHcr0AmzFrk8KaCQ==~1; bm_sz=1257C815EB51339968CA2A3C3D288D2A~YAAQtvkwF/RL+3uEAQAAUJbPiBFF5IG6RXGAZuawWliL6m39Kqt+LjJp+u5BvEMZcLIkFGsVEcsrkwXhc/EXMoj6yVhqdyw67TwWkgtjjONBbbYgNIr+zJbeeg2Jq5yWheItNnxrusydzJeMooHsNN/hZdwMiU70uPJ5jewqr9E0/ZSGw8UQDC3BcJeMpUv44cwbg4fJHNeIZT41sNNGILqSStdWMBN+HSuTDyEZ58luSmayiXR+y91aFAn8xetfqrYU2A2fhaVEGQAAO9GLJlWTGa9bJW7mOE/INoCbsPSdP7dnjnsk~3488065~3753542; hgg=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aWQiOiIyMDM5MzY3NjczNSIsImRrZS02MCI6IjI4NSIsImRrZS0xMjYiOiIzNzQiLCJka2UtMTQ0IjoiNDMxIiwiZGtlLTE0OSI6IjMzNzMiLCJka2UtMTUwIjoiNTY3IiwiZGtlLTE1MSI6IjQ1NyIsImRrZS0xNTIiOiI0NTgiLCJka2UtMTUzIjoiNDU5IiwiZGtlLTE1NCI6IjQ2MCIsImRrZS0xNTUiOiI0NjEiLCJka2UtMTU2IjoiNDYyIiwiZGtlLTE3OSI6IjU2OSIsImRrZS0yMDQiOiI3MTAiLCJka2UtMjE5IjoiMjI0NiIsImRraC0yMjkiOiJJbE5oQzA2UyIsImRrZS0yMjkiOiIwIiwiZGtlLTIzMCI6Ijg1NyIsImRrZS0yODgiOiIxMTI4IiwiZGtlLTMwMCI6IjExODgiLCJka2UtMzE4IjoiMTI2MCIsImRrZS0zNDUiOiIxMzUzIiwiZGtlLTM0NiI6IjEzNTYiLCJka2gtMzk0IjoiQ2ZYQWh6ZE8iLCJka2UtMzk0IjoiMCIsImRraC00MDgiOiJZZGFWUm1EWiIsImRrZS00MDgiOiIwIiwiZGtlLTQxNiI6IjE2NDkiLCJka2UtNDE4IjoiMTY1MSIsImRrZS00MTkiOiIxNjUyIiwiZGtlLTQyMCI6IjE2NTMiLCJka2UtNDIxIjoiMTY1NCIsImRrZS00MjIiOiIxNjU1IiwiZGtlLTQyOSI6IjE3MDUiLCJka2UtNjM2IjoiMjY5MSIsImRrZS03MDAiOiIyOTkyIiwiZGtlLTczOSI6IjMxNDAiLCJka2UtNzU3IjoiMzIxMiIsImRraC03NjgiOiJVWkdjMHJIeCIsImRrZS03NjgiOiIwIiwiZGtlLTc5MCI6IjMzNDgiLCJka2UtNzk0IjoiMzM2NCIsImRrZS04MDQiOiIzNDExIiwiZGtlLTgwNiI6IjM0MjUiLCJka2UtODA3IjoiMzQzNyIsImRrZS04MjQiOiIzNTExIiwiZGtlLTgyNSI6IjM1MTQiLCJka2UtODM0IjoiMzU1NyIsImRrZS04MzYiOiIzNTcwIiwiZGtlLTg2NSI6IjM2OTUiLCJka2gtODk1IjoiMnowRFlTQzIiLCJka2UtODk1IjoiMCIsImRrZS05MDMiOiIzODQ4IiwiZGtlLTkxNyI6IjM5MTMiLCJka2UtOTM4IjoiNDAwNCIsImRrZS05NDciOiI0MDQyIiwiZGtlLTk3NiI6IjQxNzEiLCJka2UtMTA4MSI6IjQ1ODciLCJka2UtMTEwNCI6IjQ2NzYiLCJka2UtMTEyNCI6IjQ3NjQiLCJka2UtMTEyNiI6IjQ3NjgiLCJka2gtMTEyOSI6IjI4bWhlZm9wIiwiZGtlLTExMjkiOiIwIiwiZGtzLTExNTgiOiI0OTA2IiwiZGtlLTExNzIiOiI0OTY0IiwiZGtlLTExNzMiOiI0OTY3IiwiZGtlLTExNzQiOiI0OTcwIiwiZGtlLTExODciOiI1MDE1IiwiZGtlLTEyMTAiOiI1MTI3IiwiZGtoLTEyMTEiOiJFSE5IaFNzTCIsImRrcy0xMjExIjoiMCIsImRrZS0xMjEyIjoiNTE0MSIsImRrZS0xMjEzIjoiNTE0MiIsImRrZS0xMjMxIjoiNTIxMyIsImRrZS0xMjMzIjoiNTIyMCIsImRrZS0xMjQ0IjoiNTI2NyIsImRrZS0xMjQ5IjoiNTI4OSIsImRrZS0xMjU1IjoiNTMyNiIsImRrZS0xMjU5IjoiNTMzOSIsImRrZS0xMjYxIjoiNTM0OCIsImRrZS0xMjc3IjoiNTQxMSIsImRrZS0xMjgwIjoiNTQyNyIsImRrcy0xMjg2IjoiNTQ1NSIsImRrZS0xMjg3IjoiNTQ1OCIsImRrZS0xMjkwIjoiNTQ3NSIsImRrZS0xMjk1IjoiNTQ5NSIsImRrZS0xMjcwIjoiNTM4MyIsImRrZS0xMjk5IjoiNTUxMCIsImRraC0xMzAzIjoiLUxrekFyZUsiLCJka2UtMTMwMyI6IjAiLCJka2gtMTMwNCI6IkFCSDhqM1hUIiwiZGtlLTEzMDQiOiIwIiwiZGtoLTEzMDciOiJ4UTBTSHNZOCIsImRrZS0xMzA3IjoiMCIsImRraC0xMzA4IjoiLTFHR2xmdGsiLCJka2UtMTMwOCI6IjAiLCJka3MtMTMwOSI6IjU1NTEiLCJka2UtMTMxNCI6IjU1NzMiLCJuYmYiOjE2Njg3NDI2MTYsImV4cCI6MTY2ODc0MjkxNiwiaWF0IjoxNjY4NzQyNjE2LCJpc3MiOiJkayJ9.PqKwmMrgmtmxcFxGZvKqJkOyKR7qnieLtBmnZDWgHb4'
    } 

get_tennis_events_categories_url = f"https://sportsbook-us-{region_tag}.draftkings.com//sites/US-{region_tag.upper}-SB/api/v2/displaygroupinfo?format=json"
if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

draftkings_live_tennis_url = 'https://sportsbook.draftkings.com/live?category=live-in-game&subcategory=tennis'
tennis_prefix = 'https://sportsbook.draftkings.com/event/random-shit/'


#############################

#event_ids = []
event_ids = set()
ans = collections.defaultdict(lambda: collections.defaultdict())

def get_tennis_events_categories():
    url = f"https://sportsbook-us-{region_tag}.draftkings.com//sites/US-{region_tag.upper}-SB/api/v2/displaygroupinfo?format=json"
    response = requests.request("GET", url, headers=headers, data=payload)
    print('pinging tennis main page ->',response.status_code)
    group_ids = []
    if response.status_code == 200:
        response_json = response.json()
        current_live_tennis_competitions = response_json['displayGroupInfos']

        tennis_index = 0
        for index in range(len(current_live_tennis_competitions)):
            if current_live_tennis_competitions[index]['displayName'] == 'Tennis':
                tennis_index = index
                break
        all_tennis_competitions = current_live_tennis_competitions[tennis_index]
        for tennis_competition in all_tennis_competitions['eventGroupInfos']:
            if tennis_competition['hasLiveOffers'] == True:
                group_ids.append(tennis_competition['eventGroupId'])
            
        print('tennis competitions ids (Ex: ATP world finals) ->', group_ids)
        if len(group_ids) == 0:
            print("no tennis competitions currently")
    else:
        print("Error code: Draftkings get tennis events Tier 1")
    return group_ids


async def async_get_events_from_competition(session, group_id):
    url = f"https://sportsbook-us-{region_tag}.draftkings.com//sites/US-{region_tag.upper}-SB/api/v5/eventgroups/{group_id}?format=json"
    async with session.get(url, headers=headers, data=payload) as response:
        print('response from ->', group_id, response.status)
        response_json = await response.json(content_type=None)
        #print('point of interest',response.status, type(response.status))
        if response.status == 200:
            for event in response_json['eventGroup']['events']:
                if event['eventStatus']['state'] == 'STARTED':
                    #event_ids.append(event['eventId'])
                    event_ids.add(event['eventId'])

async def async_get_event_data(session, event_id):
    url = f"https://sportsbook-us-{region_tag}.draftkings.com//sites/US-{region_tag.upper}-SB/api/v3/event/{event_id}?format=json"
    async with session.get(url, headers=headers, data=payload) as response:
        response_json = await response.json(content_type=None)
        if response.status == 200:
            ans[event_id]['url'] = tennis_prefix + event_id
            ans[event_id]['json'] = response_json

def async_dk_main():
    global event_ids
    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    start_time = time.time()
    competitions = get_tennis_events_categories()

    print("all event ids", competitions)

    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for group_id in competitions:
                tasks.append(asyncio.ensure_future(async_get_events_from_competition(session, group_id)))
            asyncio_gather = await asyncio.gather(*tasks)
        async with aiohttp.ClientSession() as session:
            tasks = []
            for event_id in event_ids:
                tasks.append(asyncio.ensure_future(async_get_event_data(session, event_id)))
            asyncio_gather = await asyncio.gather(*tasks)

    asyncio.run(main())

    print("gathered event ids", event_ids)
    with open('dk_current_event.json', 'w') as f:
        json.dump(ans, f)
        
    print("--- %s seconds ---" % (time.time() - start_time))
    return {'timestamp': timestamp, 'ans': ans}
    




if __name__ == "__main__":
    async_dk_main()