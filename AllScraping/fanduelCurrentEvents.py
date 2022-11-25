import requests
import time
import collections
import json
from datetime import datetime
import pytz

import aiohttp
import asyncio
import platform

#s3 = boto3.client("s3")
fanduel_live_tennis_url = 'https://sportsbook.fanduel.com/tennis?tab=live'
tennis_prefix = 'https://sportsbook.fanduel.com/tennis/random-shit/' #https://sportsbook.fanduel.com/tennis/random-shit/31695201
region_tag = 'nj' #'ny'

return_popular_only = False
payload={}
headers = {}

event_ids = collections.defaultdict()
ans = {}
ans = collections.defaultdict(lambda: collections.defaultdict())
sub_res = set()

if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# def Merge(dict1, dict2):
#     res = {**dict1, **dict2}
#     return res

def Merge(dict1, dict2):
    for i in dict2.keys():
        dict1[i]=dict2[i]
    return dict1

async def async_get_all_event_ids(session, group_id): #this is just the popular tab lmfao?
    global sub_res
    url =  f"https://sbapi.{region_tag}.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&_ak=FhMFpcPWXMeyZxOx&eventId={group_id}"
    async with session.get(url, headers=headers, data=payload) as response:
        response_json = await response.json(content_type=None)

        if response_json and 'layout' in response_json and 'tabs' in response_json['layout']:
            tab_ids = response_json['layout']['tabs']
            
            for tab_id in tab_ids: #not sure what this is doing
                # sub_res = tab_ids[tab_id]['title'].lower().replace(" ", "-")
                # print("sub_res", sub_res)
                sub_res.add(tab_ids[tab_id]['title'].lower().replace(" ", "-"))
            if return_popular_only:
                sub_res = ['popular']

async def async_get_event_data(session, event_id, tab_type):

    url = f"https://sbapi.{region_tag}.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&_ak=FhMFpcPWXMeyZxOx&eventId={event_id}&tab={tab_type}"
    #print("ex url", url)
    async with session.get(url, headers=headers, data=payload) as response:
        print("event data receive status",response.status, url)
        response_json = await response.json(content_type=None)

        ans[event_id]['url'] = tennis_prefix + event_id
        ans[event_id]['json'] = response_json     

        markets = ans[event_id]['json']['attachments']['markets']
        if 'markets' not in ans[event_id]:
            ans[event_id]['markets'] = {}
        for market_key in markets:
            ans[event_id]['markets'][market_key] = markets[market_key]
        #MOOSE BELOW NOT WORKING. IT IS AGGREGATING OLD DATA IN SOMEHOW. IT IS NOT REMOVING OLD LINES CLEARLY LOL
        # if event_id in ans and 'json' in ans[event_id]:
        #     #take the markets of the current one
        #     preexisting_markets = ans[event_id]['json']['attachments']['markets']
        #     new_markets_to_be_added = response_json['attachments']['markets']
        #     ans[event_id]['json']['attachments']['markets'] = Merge(preexisting_markets, new_markets_to_be_added)
        # else:
        #     ans[event_id]['json'] = response_json   
        #take this popular page and then other markets into it? 

    ans[event_id]['json']['attachments']['markets'] = ans[event_id]['markets'] 
        #we haven't tagged what hasnt been tagged yet

def get_tennis_events():
    url = f"https://sbapi.{region_tag}.sportsbook.fanduel.com/api/in-play?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&comingUpTimeRange=360000&includeStaticCards=false&language=en&regionCode=NAMERICA&timezone=America%2FNew_York&eventTypeId=2&includeTabs=false&_ak=FhMFpcPWXMeyZxOx"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.status_code)
    response_json = response.json()
    current_live_events = response_json['attachments']['events']
    events = []

    for event in current_live_events.keys():
        events.append(event)

    if len(events) == 0:
        print("no live events currently")
    return events


def async_fanduel_main():
    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    start_time = time.time()
    
    res = get_tennis_events()
    print("all event_ids", res)

    async def main():
        async with aiohttp.ClientSession() as session: #get all event ids
            tasks = []
            for event_id in res:
                tasks.append(asyncio.ensure_future(async_get_all_event_ids(session, event_id)))
                #saves results to res, but doesn't put that anywhere
            asyncio_gather = await asyncio.gather(*tasks)

        async with aiohttp.ClientSession() as session: #ping the event data
            tasks = []
            for event_id in res:
                for event_tab_type in sub_res:
                    tasks.append(asyncio.ensure_future(async_get_event_data(session, event_id, event_tab_type)))
            asyncio_gather = await asyncio.gather(*tasks)

    asyncio.run(main())
    time.sleep(0.2)
    print('sub_res', sub_res)    
    with open('fd_current_event.json', 'w') as f:
        json.dump(ans, f)
    return {'timestamp': timestamp, 'ans': ans}


if __name__ == "__main__":
    async_fanduel_main()