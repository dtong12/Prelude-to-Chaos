import requests
import collections
import json
from datetime import datetime
import pytz

import aiohttp
import asyncio
import platform

# mgm_live_tennis_url = 'https://api.ny.betmgm.com/api/v2/sports/tennis/events/nextup?limit=100'
# tennis_prefix = 'https://ny.betmgm.com/sports/tennis/'


#'tennis': {'prefix': f"https://ny.betmgm.com/sports/tennis/", 'url': f'https://api.ny.betmgm.com/api/v2/sports/tennis/events/nextup?limit=100'},


#building from scratch -> Friday november 25 2:35pm



mgm_live_tennis_url = ''
tennis_prefix = ''
region_tag = ''

payload = {}
headers = {
  'authority': 'sports.az.betmgm.com',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
  'referer': 'https://sports.az.betmgm.com/en/sports/live/tennis-5',
  'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
  'x-app-context': 'default',
  'x-bwin-browser-url': 'https://sports.az.betmgm.com/en/sports/live/tennis-5',
  'x-from-product': 'sports',
  'Cookie': '__cf_bm=wT4pX2DD2hGIldg_bDkULow8Dfsuagex3dO5P_6o3EU-1669406064-0-AWVHx3Cmr9kwtDIPd/sKSQzBkqE4Bf1c5sDTzPuWAmYu1fDBFukiGPItHm86BndikoVGiorI4pFaD9hxfDf9i4k='
}


url = "https://sports.az.betmgm.com/cds-api/bettingoffer/fixtures?x-bwin-accessid=N2Q4OGJjODYtODczMi00NjhhLWJlMWItOGY5MDUzMjYwNWM5&lang=en-us&country=US&userCountry=US&subdivision=US-Arizona&state=Live&take=50&offerMapping=Filtered&offerCategories=Gridable&sortBy=Tags&sportIds=5"

if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
ans = collections.defaultdict(lambda: collections.defaultdict())

def async_mgm_main():
    print(" /////////// BETMGM ////////////////")
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
    with open('mgm_current_event.json', 'w') as f:
        json.dump(ans, f)

    return {'timestamp': timestamp, 'ans': ans}


def get_tennis_events():
    url = "https://sports.az.betmgm.com/cds-api/bettingoffer/fixtures?x-bwin-accessid=N2Q4OGJjODYtODczMi00NjhhLWJlMWItOGY5MDUzMjYwNWM5&lang=en-us&country=US&userCountry=US&subdivision=US-Arizona&state=Live&take=50&offerMapping=Filtered&offerCategories=Gridable&sortBy=Tags&sportIds=5"
    response = requests.request("GET", url, headers=headers, data=payload)
    ans = []

    print("betmgm get_tennis_events", response.status_code)
    if response.status_code == 200:
        response_json = response.json()
        fixtures = response_json['fixtures']
        for fixture in fixtures:
            #print(fixture['id'], fixture['stage'])
            ans.append(fixture['id'])
    else:
        print("Error code: BetMGM get tennis events Tier 1")
    return ans

async def async_get_event_data(session , event_id):
    tennis_prefix = f'https://ny.betmgm.com/sports/tennis/{event_id}'
    url = f"https://sports.az.betmgm.com/cds-api/bettingoffer/fixture-view?x-bwin-accessid=N2Q4OGJjODYtODczMi00NjhhLWJlMWItOGY5MDUzMjYwNWM5&lang=en-us&country=US&userCountry=US&subdivision=US-Arizona&offerMapping=All&scoreboardMode=Full&fixtureIds={event_id}&state=Latest&includePrecreatedBetBuilder=true&supportVirtual=false&useRegionalisedConfiguration=true"
    #response = requests.request("GET", url, headers=headers, data=payload)
    async with session.get(url, headers=headers, data=payload) as response:
        print('async get event data result -> ', event_id, response.status)
        response_json = await response.json(content_type=None)
        ans[event_id]['url'] = tennis_prefix
        ans[event_id]['json'] = response_json

if __name__ == "__main__":
    async_mgm_main()
