import requests
import time
import collections
import json
from datetime import datetime
import pytz

import aiohttp
import asyncio
import platform


payload={}
headers = {
  'authority': 'nj.betrivers.com',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'referer': 'https://nj.betrivers.com/?page=sportsbook&group=1000093193&type=live',
  'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
  #'Cookie': '__cf_bm=3AuT5FmyCeBnloGH9WZ0ZKH4X.KIDW5h6zdWC2yOn_E-1669504802-0-AXgoHp068pqRd4DFUfi0EeQu/DnXS33oC8dR+efLO3Juy6j3GoekDieJXGOAeVM8WjO7B385BEi1Ru+PgJKf+30=; _cfuvid=EUxfQ3qB64aT7kit95AOprRp8xHmokKX3X0hb6edLNc-1669502496330-0-604800000'
}

event_read_headers = {
    #'Accept': 'application/json, text/javascript, */*; q=0.01',
    'accept': '*/*',
    'content-type': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://nj.betrivers.com',
    'Referer': 'https://nj.betrivers.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}

if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


ans = collections.defaultdict(lambda: collections.defaultdict())
event_ids = set()

def get_tennis_events():
    url = "https://nj.betrivers.com/apinj/service/sportsbook/offering/listview/availability?groupId=1000093193&cageCode=2"
    response = requests.request("GET", url, headers=headers, data=payload)
    print("betrivers get tennis events", response.status_code)
    ans = []
    if response.status_code == 200:
        response_json = response.json()
        competitions = response_json['live']
        for competition in competitions:
            ans.append(competition)
    else:
        print("Error code: BetRivers get tennis events Tier 1")
    return ans

async def async_get_competition_data(session, group_id): #note this only paginates by 5....
    tennis_prefix = ''
    url = f"https://nj.betrivers.com/apinj/service/sportsbook/offering/listview/events?pageNr=1&cageCode=2&groupId={group_id}&type=live"
    async with session.get(url, headers=headers, data=payload) as response:
        response_json = await response.json(content_type=None)
        for item in response_json['items']:
            event_ids.add(item['id'])

async def async_get_event_data(session, event_id):
    url = f"https://eu-offering.kambicdn.org/offering/v2018/rsiusnj/betoffer/event/{event_id}.json?lang=en_US&market=US-NJ&client_id=2&channel_id=1&ncid=1669508557208&includeParticipants=true"
    async with session.get(url, headers=event_read_headers, data=payload) as response:
        response_json = await response.json(content_type=None)
        print(event_id, response.status)
        ans[event_id]['url'] = url
        ans[event_id]['json'] = response_json

def async_betrivers_main():
    print(" /////////// BETRIVERS ////////////////")
    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    start_time = time.time()
    
    res = get_tennis_events()
    print("all competition_ids", res)

    async def main():
        async with aiohttp.ClientSession() as session: #get all event ids
            tasks = []
            for event_id in res:
                tasks.append(asyncio.ensure_future(async_get_competition_data(session, event_id)))
            asyncio_gather = await asyncio.gather(*tasks)
        
        print('event ids stored from competition ids',event_ids)
        async with aiohttp.ClientSession() as session: #get all event ids
            tasks = []
            for event_id in event_ids:
                tasks.append(asyncio.ensure_future(async_get_event_data(session, event_id)))
            asyncio_gather = await asyncio.gather(*tasks)

    asyncio.run(main())
    with open('betrivers_current_event.json', 'w') as f:
        json.dump(ans, f)
    return {'timestamp': timestamp, 'ans': ans}

if __name__ == '__main__':
    async_betrivers_main()
    # get_tennis_events()
