import requests
import collections
import json
from datetime import datetime
import pytz

import aiohttp
import asyncio
import platform


barstool_live_tennis_url = ''
tennis_prefix  = ''
region_tag = ''

payload={}
headers = {
  'Accept': 'application/json, text/plain, */*',
  'content-type': 'application/json',
  'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'Connection': 'keep-alive',
  'Origin': 'https://www.barstoolsportsbook.com',
  'Referer': 'https://www.barstoolsportsbook.com/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'cross-site',
  'User-Agent': 'Mozislla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"'
}

if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
ans = collections.defaultdict(lambda: collections.defaultdict())


def get_tennis_events():
    url = "https://eu-offering.kambicdn.org/offering/v2018/pivusaz/event/live/open.json?depth=2&includeParticipants=true&lang=en_US&market=US"
    response = requests.request("GET", url, headers=headers, data=payload)

    response_json = response.json()
    res = []
    for liveEvent in response_json['liveEvents']:
        #print(liveEvent['event']['sport'])
        if liveEvent['event']['sport'] == 'TENNIS':
            #print(liveEvent['event']['id'])
            res.append(liveEvent['event']['id'])
    return res

async def async_get_event_data(session, event_id):
    url = f"https://eu-offering.kambicdn.org/offering/v2018/pivusaz/betoffer/event/{event_id}?type=&includeParticipants=true&lang=en_US&market=US"
    print(url)
    async with session.get(url, headers=headers, data=payload) as response:
        print(event_id, response.status)
        response_json = await response.json(content_type=None)
        ans[event_id]['url'] = tennis_prefix
        ans[event_id]['json'] = response_json


def async_barstool_main():
    print(" /////////// BARSTOOLS ////////////////")
    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    event_ids = get_tennis_events()
    print("ASYNC EVENT IDS", event_ids)
    async def main():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for event_id in event_ids:
                tasks.append(asyncio.ensure_future(async_get_event_data(session, event_id)))
            asyncio_gather = await asyncio.gather(*tasks)
    asyncio.run(main())
    with open('barstools_current_event.json', 'w') as f:
        json.dump(ans, f)
    return {'timestamp': timestamp, 'ans': ans}

if __name__ == '__main__':
    async_barstool_main()
    # test_current_response()





