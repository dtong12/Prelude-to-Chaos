import requests
import time
import collections
import json
from datetime import datetime
import pytz

#s3 = boto3.client("s3")
fanduel_live_tennis_url = 'https://sportsbook.fanduel.com/tennis?tab=live'
tennis_prefix = 'https://sportsbook.fanduel.com/tennis/random-shit/' #https://sportsbook.fanduel.com/tennis/random-shit/31695201


def fanduel_main():
    bucket = 'tennis-pipeline'
    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%m_%d_%Y_ %H:%M:%S")
    latest_file_name = f'latest-data/fanduel_current' + '.json'
    historic_file_name = f'historic-data/fanduel-historic-data/{timestamp}_fanduel_historic' + '.json'

    ans = collections.defaultdict()

    res = get_tennis_events()
    print("all event_ids", res)
    for event_id in res:
        event_tab_types = get_all_event_ids(event_id) 
        for event_tab_type in event_tab_types:
            event_data_json = get_event_data(event_id, event_tab_type)

            if event_id not in ans:
                ans[event_id] = {}
            ans[event_id]['url'] = tennis_prefix + event_id
            ans[event_id]['json'] = event_data_json
    return {'timestamp': timestamp, 'ans': ans}
    

def get_tennis_events():
    url = "https://sbapi.ny.sportsbook.fanduel.com/api/in-play?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&comingUpTimeRange=360000&includeStaticCards=false&language=en&regionCode=NAMERICA&timezone=America%2FNew_York&eventTypeId=2&includeTabs=false&_ak=FhMFpcPWXMeyZxOx"
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


def get_all_event_ids(event_id, return_popular_only = True):
    print("event _id", event_id)
    url = f"https://sbapi.ny.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&_ak=FhMFpcPWXMeyZxOx&eventId={event_id}"
    print("url", url)
    payload={}
    headers = {}
    res = []
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = response.json()

    tab_ids = response_json['layout']['tabs']

    for tab_id in tab_ids:
        res = tab_ids[tab_id]['title'].lower().replace(" ", "-")

    if return_popular_only:
        return ['popular']

    return res


def get_event_data(event_id, tabType):
    url = f"https://sbapi.ny.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&_ak=FhMFpcPWXMeyZxOx&eventId={event_id}&tab={tabType}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print("event data receive status",response.status_code)
    return response.json()

if __name__ == "__main__":
    res = fanduel_main()

    res_json = res['ans']
    with open('fd_current_event.json', 'w') as f:
        json.dump(res_json, f)
