import requests
import time
import collections
import json
from datetime import datetime
import pytz


#s3 = boto3.client("s3")
caesars_live_tennis_url = 'https://www.williamhill.com/us/ny/bet/tennis/inplay'




def caesars_main():

    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    ans = collections.defaultdict()
    event_ids = get_tennis_events()
    for event_id in event_ids:
        tennis_prefix = f'https://www.williamhill.com/us/ny/bet/tennis/{event_id}/rand'
        event_data_json = get_event_data(event_id)
        if event_id not in ans:
            ans[event_id] = {}
        ans[event_id]['url'] = tennis_prefix
        ans[event_id]['json'] = event_data_json
    return {'timestamp': timestamp, 'ans': ans}


def get_tennis_events():
    url = "https://www.williamhill.com/us/ny/bet/api/v3/sports/tennis/events/in-play"

    payload={}
    headers = {
    'authority': 'www.williamhill.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'content-type': 'application/json',
    'cookie': '_gcl_au=1.1.158980712.1658693276; _scid=abcc6923-3c55-4077-91ae-f4c1571e76e5; _mkto_trk=id:580-JWZ-774&token:_mch-williamhill.com-1658693276967-64758; afUserId=5e616c9e-ea80-4f72-aa1c-a6ee75a46b55-p; optimizelyEndUserId=oeu1658693291262r0.686850182161177; _ALGOLIA=anonymous-14db2454-2c4e-40c9-b4f4-2b1b6cc96415; UniqueDeviceId=abb9a280-6ae3-4119-beb3-6bba7cf930b8; wf_cookie_bc=CZRFULL; AMCVS_05C8485451E452E30A490D45%40AdobeOrg=1; s_cc=true; AF_SYNC=1661723294445; _sctr=1|1661659200000; AMCV_05C8485451E452E30A490D45%40AdobeOrg=1176715910%7CMCIDTS%7C19235%7CMCMID%7C23774548134237944860170808146509853427%7CMCAAMLH-1662431671%7C7%7CMCAAMB-1662431671%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1661834071s%7CNONE%7CvVersion%7C5.4.0; _gid=GA1.2.1954238850.1661826872; fs_uid=#1388JK#4775353015013376:5939604813942784:::#/1690229276; _clck=19ohx9e|1|f4g|0; TS018bddb2=0109a8365725ca12b4cf0b29ae33dede80d32c1757f8e47b97eb1dde304d2f0169e4f990e3ce2a104b0a59bad949b47e74776ab6cf; s_sq=%5B%5BB%5D%5D; _clsk=1cxs3j6|1661826911580|9|0|h.clarity.ms/collect; _dc_gtm_UA-136626402-7=1; _ga_PPYR8MS1KL=GS1.1.1661826872.8.1.1661826955.57.0.0; _ga=GA1.1.39755854350.1658693275973; _uetsid=47bb82a0280c11edb51d2f599ff6c025; _uetvid=4eb459f00b8c11edaf14f5e880ba57f6',
    'referer': 'https://www.williamhill.com/us/ny/bet/tennis/inplay',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response_json = response.json()
    ans = []
    competitions = response_json['competitions']

    for competition in competitions:
        for event in competition['events']:
            ans.append(event['id'])
    print(ans)
    return ans


def get_event_data(event_id):

    url = f"https://www.williamhill.com/us/ny/bet/api/v3/events/{event_id}"

    payload={}
    headers = {
    'authority': 'www.williamhill.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'content-type': 'application/json',
    'referer': 'https://www.williamhill.com/us/ny/bet/tennis/78a39860-7853-47ff-a20e-b0627d922f8a/nick-kyrgios-vs-thanasi-kokkinakis',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(event_id, "->", response.status_code)
    return response.json()

def lambda_handler(event, context):
    bucket = 'tennis-pipeline'
    # timestamp = datetime.now().strftime("%m_%d_%Y_ %H:%M:%S")
    timestamp = datetime.now().strftime("%Y_%m_%d %H:%M:%S")
    latest_file_name = f'latest-data/caesars_current' + '.json'
    historic_file_name = f'historic-data/caesars-historic-data/{timestamp}_caesars_historic' + '.json'

    ans = collections.defaultdict()
    event_ids = get_tennis_events()
    for event_id in event_ids:
        tennis_prefix = f'https://www.williamhill.com/us/ny/bet/tennis/{event_id}/rand'
        event_data_json = get_event_data(event_id)
        if event_id not in ans:
            ans[event_id] = {}
        ans[event_id]['url'] = tennis_prefix
        ans[event_id]['json'] = event_data_json

    # uploadByteStream = bytes(json.dumps(ans).encode("UTF-8"))
    # s3.put_object(Bucket = bucket, Key =  latest_file_name, Body = uploadByteStream)
    # s3.put_object(Bucket = bucket, Key =  historic_file_name, Body = uploadByteStream)
    # print("Put complete")
    return True

if __name__ == "__main__":
    # caesars_main()
    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    ans = collections.defaultdict()
    event_ids = get_tennis_events()
    for event_id in event_ids:
        tennis_prefix = f'https://www.williamhill.com/us/ny/bet/{event_id}/rand'
        event_data_json = get_event_data(event_id)
        if event_id not in ans:
            ans[event_id] = {}
        ans[event_id]['url'] = tennis_prefix
        ans[event_id]['json'] = event_data_json
    

    with open('ca_current_event.json', 'w') as f:
        json.dump(ans, f)