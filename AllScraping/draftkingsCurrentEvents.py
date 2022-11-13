import requests
import collections
import json
from datetime import datetime
import pytz


#s3 = boto3.client("s3")
draftkings_live_tennis_url = 'https://sportsbook.draftkings.com/live?category=live-in-game&subcategory=tennis'
tennis_prefix = 'https://sportsbook.draftkings.com/event/random-shit/' #https://sportsbook.fanduel.com/tennis/random-shit/31695201

def dk_main():
    
    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    array_of_group_ids = get_tennis_events_categories()
    event_ids = get_events_from_competition(array_of_group_ids)

    ans = collections.defaultdict()
    for event_id in event_ids:
        if event_id not in ans: 
            ans[event_id] = {}
        ans[event_id]['url'] = tennis_prefix + event_id
        ans[event_id]['json'] = get_event_data(event_id)
    
    return {'timestamp': timestamp, 'ans': ans}



def get_tennis_events_categories():
    url = "https://sportsbook-us-ny.draftkings.com//sites/US-NY-SB/api/v2/displaygroupinfo?format=json"

    payload={}
    headers = {
    'authority': 'sportsbook-us-ny.draftkings.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'origin': 'https://sportsbook.draftkings.com',
    'referer': 'https://sportsbook.draftkings.com/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Cookie': 'STE="2022-08-30T02:05:01.8667669Z"; STH=88daae768db8fb9e6a405800b36e7a97e29d6887d42a9de70174864fc2959324; STIDN=eyJDIjoxMjIzNTQ4NTIzLCJTIjozNjM0MzE2MTg3NywiU1MiOjM4MzA0MjAyODk0LCJWIjoyMDM5MzY3NjczNSwiTCI6MSwiRSI6IjIwMjItMDgtMzBUMDI6MDU6MDEuODY2NzY2OVoiLCJTRSI6IlVTLURLIiwiVUEiOiJzcjBoRDVURXBGNE1DMVlFdW5zLzZpR2h3em5uOXlvTnVZMkNSTFJSMFpjPSIsIkRLIjoiY2FkN2RkNGUtMzQ1NS00N2YwLTkwNGUtZDJkZjJmN2I1OTExIiwiREkiOiI5YWFjNjY1Ny1jMTIxLTRlNmUtYjA4ZC03ZDk3YjJjYzM0OTEiLCJERCI6MTg0ODI2NDU2Mzl9; _abck=08C127B41C6047E3A38AF5AC0AF6F2B5~-1~YAAQiJs+FxzXVtiCAQAAcjlj7AhTkwmvihlGmmCBG7Nr+LtBDRSoN8dh0WVMuIYx754ImJP/fNam0FLxsi8ePZbF956ZbznVqncpvJcTGet1DIbQti4rurPjEfICMLT0MF7zNOirewIc5DJ8z7xBs1tZKgC0X2dhHbKIgAbyLU//K3FRygixakQffcv8CYgxtADw2SomBla64kUUyFK9YGwZYIh5J798IHVBxbvOaQIk9nef1g7oJbWHjoo4QSDn0PRev1VVSmielWlTKVspNlL9g9+8lEnVyxOHYROI0VnkGZJRLweHeXlwQcSXYr5eLOdYLmtNJS+iOWLVQKG9sLBTcaYatnL/D2ULYOzqwYpJJrO7BmkcULnHz17mJ0vim9vcwhsxGlYlOACoJFlT1DuHcOtSdFcOXa0aBLg=~-1~-1~-1; _csrf=9a233680-b502-417a-a37d-ca0e64218adb; ak_bmsc=63678F2CB9CD0D822552FBBF655540D4~000000000000000000000000000000~YAAQiJs+Fx3XVtiCAQAAcjlj7BBk4QtAyrdMMxgRzE/6vHSybzRvRENgBLlTAczHjIyKLYuihhVW0X0IgW/sIeBgKSLnr/qEdqmX18fwm8809nXy3xyfb8AWRoqGSsiQIGd67k7R/iOMjPUhr1LyQUMstHeVyH1c3AMq+OntPBTtKrhTvA2T0OMLSFx6egSPnSVIVdWV7tFYlb31Bu/15glUEWU0gyybhXsIIprFFyLKnL44bAwrw3Y/ufO4Hc6zoSfHMHTGPTNZ5RTkiAfRRkzqMikrwIHB6rNAbr2yq0ws2k/16EVeTSRaXMOe153jhZSgvVZotWZSziXDwakUG2UDifDodeoHjugwXqoE9tuchZ42+FceN8bYNxYxGM8=; bm_sz=E7FF7033AB53F281352D962AD2998D74~YAAQiJs+Fx7XVtiCAQAAcjlj7BBFmZCFsilvOjSbaNbzdQCwrynEkTYlqa+jtaan0eOS97Hcc32jLImi31WlwibTZIjQ2YM9ys5SJGqNBkTPiOQaC+Dkyzsk8K/8luUUFdzHTZUWwPuPDf+X4erJtcht3bmu+P1zxB4FsRqoTZH+ixAForI+0b3JfpD8esPWYq8TYtLFaHvWOc0PgPgjOqT8WP+9rDBvvDktxRkgsBIlXLwqwDDVs+xS3x+TlD3h1jEhw5XoLjqWrZyMSFpvD9c906oYK3YvSEqlBFgmzD5E1tsIBLHH~3486003~3225924; hgg=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aWQiOiIyMDM5MzY3NjczNSIsImRrZS02MCI6IjI4NSIsImRrZS0xMjYiOiIzNzQiLCJka2UtMTQ0IjoiNDMxIiwiZGtlLTE0OSI6IjMzNzMiLCJka2UtMTUwIjoiNTY3IiwiZGtlLTE1MSI6IjQ1NyIsImRrZS0xNTIiOiI0NTgiLCJka2UtMTUzIjoiNDU5IiwiZGtlLTE1NCI6IjQ2MCIsImRrZS0xNTUiOiI0NjEiLCJka2UtMTU2IjoiNDYyIiwiZGtlLTE3OSI6IjU2OSIsImRrZS0yMDQiOiI3MTAiLCJka2UtMjE5IjoiMjI0NiIsImRraC0yMjkiOiJJbE5oQzA2UyIsImRrZS0yMjkiOiIwIiwiZGtlLTIzMCI6Ijg1NyIsImRrZS0yODgiOiIxMTI4IiwiZGtlLTMwMCI6IjExODgiLCJka2UtMzE4IjoiMTI2MCIsImRrZS0zNDUiOiIxMzUzIiwiZGtlLTM0NiI6IjEzNTYiLCJka2gtMzk0IjoiQ2ZYQWh6ZE8iLCJka2UtMzk0IjoiMCIsImRraC00MDgiOiJZZGFWUm1EWiIsImRrZS00MDgiOiIwIiwiZGtlLTQxNiI6IjE2NDkiLCJka2UtNDE4IjoiMTY1MSIsImRrZS00MTkiOiIxNjUyIiwiZGtlLTQyMCI6IjE2NTMiLCJka2UtNDIxIjoiMTY1NCIsImRrZS00MjIiOiIxNjU1IiwiZGtlLTQyOSI6IjE3MDUiLCJka2UtNjM2IjoiMjY5MSIsImRrZS03MDAiOiIyOTkyIiwiZGtlLTczOSI6IjMxNDAiLCJka2UtNzU3IjoiMzIxMiIsImRraC03NjgiOiJVWkdjMHJIeCIsImRrZS03NjgiOiIwIiwiZGtlLTc5MCI6IjMzNDgiLCJka2UtNzk0IjoiMzM2NCIsImRrZS04MDQiOiIzNDExIiwiZGtlLTgwNiI6IjM0MjUiLCJka2UtODA3IjoiMzQzNyIsImRrZS04MjQiOiIzNTExIiwiZGtlLTgyNSI6IjM1MTQiLCJka2UtODM0IjoiMzU1NyIsImRrZS04MzYiOiIzNTcwIiwiZGtlLTg2NSI6IjM2OTUiLCJka2gtODk1IjoiMnowRFlTQzIiLCJka2UtODk1IjoiMCIsImRrZS05MDMiOiIzODQ4IiwiZGtlLTkxNyI6IjM5MTMiLCJka2UtOTE4IjoiMzkxNyIsImRrZS05MjQiOiIzOTQyIiwiZGtlLTkzOCI6IjQwMDQiLCJka2UtOTQ3IjoiNDA0MiIsImRrZS05NzYiOiI0MTcxIiwiZGtlLTk5MyI6IjQyNDAiLCJka2gtMTAwNSI6ImRyWW5oVUUxIiwiZGtlLTEwMDUiOiIwIiwiZGtlLTEwMDgiOiI0MzA1IiwiZGtlLTEwODEiOiI0NTg3IiwiZGtlLTExMDQiOiI0Njc2IiwiZGtlLTExMjQiOiI0NzY0IiwiZGtlLTExMjUiOiI0NzY1IiwiZGtlLTExMjYiOiI0NzY4IiwiZGtlLTExMjciOiI0NzczIiwiZGtoLTExMjkiOiIyOG1oZWZvcCIsImRrZS0xMTI5IjoiMCIsImRrZS0xMTMwIjoiNDc4NCIsImRrZS0xMTU4IjoiNDkwNiIsImRrZS0xMTU5IjoiNDkwOCIsImRrZS0xMTcyIjoiNDk2NCIsImRrZS0xMTczIjoiNDk2NyIsImRrZS0xMTc0IjoiNDk3MCIsImRrZS0xMTg3IjoiNTAxNSIsImRraC0xMTkxIjoiMXpTX3hlVmMiLCJka3MtMTE5MSI6IjAiLCJka2UtMTIxMCI6IjUxMjciLCJka2gtMTIxMSI6ImVHU0R4czhpIiwiZGtlLTEyMTEiOiIwIiwiZGtlLTEyMTIiOiI1MTQxIiwiZGtlLTEyMTMiOiI1MTQyIiwiZGtoLTEyMTkiOiJCeUhTWll4NiIsImRrZS0xMjE5IjoiMCIsImRraC0xMjIxIjoiMWVrSms0My0iLCJka2UtMTIyMSI6IjAiLCJka2UtMTIyMyI6IjUxNzciLCJka2UtMTIyNCI6IjUxODAiLCJka2gtMTIyNyI6IndCZFduYXozIiwiZGtlLTEyMjciOiIwIiwiZGtoLTEyMjgiOiJMM0J6TnQtUyIsImRrZS0xMjI4IjoiMCIsImRraC0xMjMxIjoiRzNlNzNTYXAiLCJka2UtMTIzMSI6IjAiLCJka2gtMTIzMiI6ImpFci1HTWkzIiwiZGtlLTEyMzIiOiIwIiwiZGtlLTEyMzMiOiI1MjIwIiwiZGtzLTEyMzQiOiI1MjI0IiwiZGtzLTEyMzciOiI1MjM3IiwiZGtlLTEyMzgiOiI1MjQwIiwiZGtzLTEyNDAiOiI1MjQ3IiwiZGtlLTEyNDIiOiI1MjU4IiwibmJmIjoxNjYxODIzMzAxLCJleHAiOjE2NjE4MjM2MDEsImlhdCI6MTY2MTgyMzMwMSwiaXNzIjoiZGsifQ.guxD_fOjAOgNoYK0E6Wj8kFaiDWppKBuLF_CTVA-OIA'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print('pinging tennis main page ->',response.status_code)

    response_json = response.json()
    current_live_tennis_competitions = response_json['displayGroupInfos']

    tennis_index = 0
    for index in range(len(current_live_tennis_competitions)):
        if current_live_tennis_competitions[index]['displayName'] == 'Tennis':
            tennis_index = index
            break
    group_ids = []
    all_tennis_competitions = current_live_tennis_competitions[tennis_index]
    for tennis_competition in all_tennis_competitions['eventGroupInfos']:
        if tennis_competition['hasLiveOffers'] == True:
            group_ids.append(tennis_competition['eventGroupId'])
        
    print('tennis competitions ->', group_ids)


    if len(group_ids) == 0:
        print("no tennis competitions currently")
    return group_ids

def get_events_from_competition(array_of_group_ids):
    payload={}
    headers = {
    'authority': 'sportsbook-us-ny.draftkings.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'origin': 'https://sportsbook.draftkings.com',
    'referer': 'https://sportsbook.draftkings.com/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Cookie': 'STE="2022-08-30T02:20:31.5784683Z"; STH=88daae768db8fb9e6a405800b36e7a97e29d6887d42a9de70174864fc2959324; STIDN=eyJDIjoxMjIzNTQ4NTIzLCJTIjozNjM0MzE2MTg3NywiU1MiOjM4MzA0MjAyODk0LCJWIjoyMDM5MzY3NjczNSwiTCI6MSwiRSI6IjIwMjItMDgtMzBUMDI6MDU6MDEuODY2NzY2OVoiLCJTRSI6IlVTLURLIiwiVUEiOiJzcjBoRDVURXBGNE1DMVlFdW5zLzZpR2h3em5uOXlvTnVZMkNSTFJSMFpjPSIsIkRLIjoiY2FkN2RkNGUtMzQ1NS00N2YwLTkwNGUtZDJkZjJmN2I1OTExIiwiREkiOiI5YWFjNjY1Ny1jMTIxLTRlNmUtYjA4ZC03ZDk3YjJjYzM0OTEiLCJERCI6MTg0ODI2NDU2Mzl9; _abck=08C127B41C6047E3A38AF5AC0AF6F2B5~-1~YAAQiJs+FxzXVtiCAQAAcjlj7AhTkwmvihlGmmCBG7Nr+LtBDRSoN8dh0WVMuIYx754ImJP/fNam0FLxsi8ePZbF956ZbznVqncpvJcTGet1DIbQti4rurPjEfICMLT0MF7zNOirewIc5DJ8z7xBs1tZKgC0X2dhHbKIgAbyLU//K3FRygixakQffcv8CYgxtADw2SomBla64kUUyFK9YGwZYIh5J798IHVBxbvOaQIk9nef1g7oJbWHjoo4QSDn0PRev1VVSmielWlTKVspNlL9g9+8lEnVyxOHYROI0VnkGZJRLweHeXlwQcSXYr5eLOdYLmtNJS+iOWLVQKG9sLBTcaYatnL/D2ULYOzqwYpJJrO7BmkcULnHz17mJ0vim9vcwhsxGlYlOACoJFlT1DuHcOtSdFcOXa0aBLg=~-1~-1~-1; _csrf=9a233680-b502-417a-a37d-ca0e64218adb; ak_bmsc=63678F2CB9CD0D822552FBBF655540D4~000000000000000000000000000000~YAAQiJs+Fx3XVtiCAQAAcjlj7BBk4QtAyrdMMxgRzE/6vHSybzRvRENgBLlTAczHjIyKLYuihhVW0X0IgW/sIeBgKSLnr/qEdqmX18fwm8809nXy3xyfb8AWRoqGSsiQIGd67k7R/iOMjPUhr1LyQUMstHeVyH1c3AMq+OntPBTtKrhTvA2T0OMLSFx6egSPnSVIVdWV7tFYlb31Bu/15glUEWU0gyybhXsIIprFFyLKnL44bAwrw3Y/ufO4Hc6zoSfHMHTGPTNZ5RTkiAfRRkzqMikrwIHB6rNAbr2yq0ws2k/16EVeTSRaXMOe153jhZSgvVZotWZSziXDwakUG2UDifDodeoHjugwXqoE9tuchZ42+FceN8bYNxYxGM8=; bm_sv=6CFC95F57B262001EC4DFB1412897C4A~YAAQtE/eF1HJbLaCAQAAKGlx7BCLR59ZwargUMjd5UOxnldQW8QBAwQpktm2qLHkUb238iMRBDuzW/aAnCBrGGsbB1H2R7GLvRZbwCR8g4dVaUWpULczln5jNL8ONseckbFZ4P0JQlvmDd7SWJ3SFtIvEKZutnUwJTES0MHHWKiJ9TOeFTF0aS7oewsmwOA7tHozSN6XBw1FkWWKgcyCupXsBW0soFqLvPONjROJiTGZcLWjwdjpuAgKu03yJ5r5ZvPQfQ==~1; bm_sz=E7FF7033AB53F281352D962AD2998D74~YAAQiJs+Fx7XVtiCAQAAcjlj7BBFmZCFsilvOjSbaNbzdQCwrynEkTYlqa+jtaan0eOS97Hcc32jLImi31WlwibTZIjQ2YM9ys5SJGqNBkTPiOQaC+Dkyzsk8K/8luUUFdzHTZUWwPuPDf+X4erJtcht3bmu+P1zxB4FsRqoTZH+ixAForI+0b3JfpD8esPWYq8TYtLFaHvWOc0PgPgjOqT8WP+9rDBvvDktxRkgsBIlXLwqwDDVs+xS3x+TlD3h1jEhw5XoLjqWrZyMSFpvD9c906oYK3YvSEqlBFgmzD5E1tsIBLHH~3486003~3225924; hgg=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aWQiOiIyMDM5MzY3NjczNSIsImRrZS02MCI6IjI4NSIsImRrZS0xMjYiOiIzNzQiLCJka2UtMTQ0IjoiNDMxIiwiZGtlLTE0OSI6IjMzNzMiLCJka2UtMTUwIjoiNTY3IiwiZGtlLTE1MSI6IjQ1NyIsImRrZS0xNTIiOiI0NTgiLCJka2UtMTUzIjoiNDU5IiwiZGtlLTE1NCI6IjQ2MCIsImRrZS0xNTUiOiI0NjEiLCJka2UtMTU2IjoiNDYyIiwiZGtlLTE3OSI6IjU2OSIsImRrZS0yMDQiOiI3MTAiLCJka2UtMjE5IjoiMjI0NiIsImRraC0yMjkiOiJJbE5oQzA2UyIsImRrZS0yMjkiOiIwIiwiZGtlLTIzMCI6Ijg1NyIsImRrZS0yODgiOiIxMTI4IiwiZGtlLTMwMCI6IjExODgiLCJka2UtMzE4IjoiMTI2MCIsImRrZS0zNDUiOiIxMzUzIiwiZGtlLTM0NiI6IjEzNTYiLCJka2gtMzk0IjoiQ2ZYQWh6ZE8iLCJka2UtMzk0IjoiMCIsImRraC00MDgiOiJZZGFWUm1EWiIsImRrZS00MDgiOiIwIiwiZGtlLTQxNiI6IjE2NDkiLCJka2UtNDE4IjoiMTY1MSIsImRrZS00MTkiOiIxNjUyIiwiZGtlLTQyMCI6IjE2NTMiLCJka2UtNDIxIjoiMTY1NCIsImRrZS00MjIiOiIxNjU1IiwiZGtlLTQyOSI6IjE3MDUiLCJka2UtNjM2IjoiMjY5MSIsImRrZS03MDAiOiIyOTkyIiwiZGtlLTczOSI6IjMxNDAiLCJka2UtNzU3IjoiMzIxMiIsImRraC03NjgiOiJVWkdjMHJIeCIsImRrZS03NjgiOiIwIiwiZGtlLTc5MCI6IjMzNDgiLCJka2UtNzk0IjoiMzM2NCIsImRrZS04MDQiOiIzNDExIiwiZGtlLTgwNiI6IjM0MjUiLCJka2UtODA3IjoiMzQzNyIsImRrZS04MjQiOiIzNTExIiwiZGtlLTgyNSI6IjM1MTQiLCJka2UtODM0IjoiMzU1NyIsImRrZS04MzYiOiIzNTcwIiwiZGtlLTg2NSI6IjM2OTUiLCJka2gtODk1IjoiMnowRFlTQzIiLCJka2UtODk1IjoiMCIsImRrZS05MDMiOiIzODQ4IiwiZGtlLTkxNyI6IjM5MTMiLCJka2UtOTE4IjoiMzkxNyIsImRrZS05MjQiOiIzOTQyIiwiZGtlLTkzOCI6IjQwMDQiLCJka2UtOTQ3IjoiNDA0MiIsImRrZS05NzYiOiI0MTcxIiwiZGtlLTk5MyI6IjQyNDAiLCJka2gtMTAwNSI6ImRyWW5oVUUxIiwiZGtlLTEwMDUiOiIwIiwiZGtlLTEwMDgiOiI0MzA1IiwiZGtlLTEwODEiOiI0NTg3IiwiZGtlLTExMDQiOiI0Njc2IiwiZGtlLTExMjQiOiI0NzY0IiwiZGtlLTExMjUiOiI0NzY1IiwiZGtlLTExMjYiOiI0NzY4IiwiZGtlLTExMjciOiI0NzczIiwiZGtoLTExMjkiOiIyOG1oZWZvcCIsImRrZS0xMTI5IjoiMCIsImRrZS0xMTMwIjoiNDc4NCIsImRrZS0xMTU4IjoiNDkwNiIsImRrZS0xMTU5IjoiNDkwOCIsImRrZS0xMTcyIjoiNDk2NCIsImRrZS0xMTczIjoiNDk2NyIsImRrZS0xMTc0IjoiNDk3MCIsImRrZS0xMTg3IjoiNTAxNSIsImRraC0xMTkxIjoiMXpTX3hlVmMiLCJka3MtMTE5MSI6IjAiLCJka2UtMTIxMCI6IjUxMjciLCJka2gtMTIxMSI6ImVHU0R4czhpIiwiZGtlLTEyMTEiOiIwIiwiZGtlLTEyMTIiOiI1MTQxIiwiZGtlLTEyMTMiOiI1MTQyIiwiZGtoLTEyMTkiOiJCeUhTWll4NiIsImRrZS0xMjE5IjoiMCIsImRraC0xMjIxIjoiMWVrSms0My0iLCJka2UtMTIyMSI6IjAiLCJka2UtMTIyMyI6IjUxNzciLCJka2UtMTIyNCI6IjUxODAiLCJka2gtMTIyNyI6IndCZFduYXozIiwiZGtlLTEyMjciOiIwIiwiZGtoLTEyMjgiOiJMM0J6TnQtUyIsImRrZS0xMjI4IjoiMCIsImRraC0xMjMxIjoiRzNlNzNTYXAiLCJka2UtMTIzMSI6IjAiLCJka2gtMTIzMiI6ImpFci1HTWkzIiwiZGtlLTEyMzIiOiIwIiwiZGtlLTEyMzMiOiI1MjIwIiwiZGtzLTEyMzQiOiI1MjI0IiwiZGtzLTEyMzciOiI1MjM3IiwiZGtlLTEyMzgiOiI1MjQwIiwiZGtzLTEyNDAiOiI1MjQ3IiwiZGtlLTEyNDIiOiI1MjU4IiwibmJmIjoxNjYxODI0MjA2LCJleHAiOjE2NjE4MjQ1MDYsImlhdCI6MTY2MTgyNDIwNiwiaXNzIjoiZGsifQ.FR60r6cO5YT-tfPWXT2Kpxztd4Tr418K4X_pF9DvcEI'
    }

    event_ids = []

    for group_id in array_of_group_ids:
        url = f"https://sportsbook-us-ny.draftkings.com//sites/US-NY-SB/api/v5/eventgroups/{group_id}?format=json"
        response = requests.request("GET", url, headers=headers, data=payload)
        print('response from ->',group_id, response.status_code)
        response_json = response.json()

        for event in response_json['eventGroup']['events']:
            if event['eventStatus']['state'] == 'STARTED':
                event_ids.append(event['eventId'])
    print(event_ids)
    return event_ids

def get_event_data(event_id):
    url = f"https://sportsbook-us-ny.draftkings.com//sites/US-NY-SB/api/v3/event/{event_id}?format=json"

    payload={}
    headers = {
    'authority': 'sportsbook-us-ny.draftkings.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cookie': 'VIDN=20361385836; SN=1223548523; LID=1; SINFN=PID=&AOID=&PUID=0&SSEG=&GLI=0&LID=1&site=US-DK; _gcl_au=1.1.1656719132.1658367416; _rdt_uuid=1658367416674.c956b1a6-fda1-4009-bdfc-a45532ae3798; ajs_group_id=null; ajs_user_id=null; ajs_anonymous_id=%22679e8abb-4fd9-463d-989f-93928112cbba%22; __qca=P0-449245438-1658367417044; _tt_enable_cookie=1; _ttp=7c090a32-bc1b-40aa-b42f-f2a5b8716df0; _scid=f79b587d-9714-4e52-a18d-426b33cc2e96; _hjSessionUser_2150570=eyJpZCI6ImQ2NmE1MGJiLTNhOWQtNTI4MS05M2Y4LTRhN2VlNThhOTE1MyIsImNyZWF0ZWQiOjE2NTgzNjc0MjUwNzksImV4aXN0aW5nIjp0cnVlfQ==; __ssid=0a9d9a833c9e96e3bd7059008b53939; _hjSessionUser_2068042=eyJpZCI6Ijk0OTRhYzg2LTdlMjUtNWFiOS1iNWJkLTc1OWZhOTAyYmY0ZSIsImNyZWF0ZWQiOjE2NTgzNjc0MTcwMjksImV4aXN0aW5nIjp0cnVlfQ==; site=US-DK; networkType=cable; _csrf=8c9a7f1a-a507-4593-9050-49afb03abd8c; notice_behavior=implied,eu; _sctr=1|1661486400000; _gid=GA1.2.1174755083.1661723162; STIDN=eyJDIjoxMjIzNTQ4NTIzLCJTIjozNjMxMTkwODc1OCwiU1MiOjM4MjcxNDAzMDUzLCJWIjoyMDM2MTM4NTgzNiwiTCI6MSwiRSI6IjIwMjItMDgtMjlUMDg6MTY6NDQuOTMxMTAxMVoiLCJTRSI6IlVTLURLIiwiVUEiOiJzcjBoRDVURXBGNE1DMVlFdW5zLzZpR2h3em5uOXlvTnVZMkNSTFJSMFpjPSIsIkRLIjoiMTM1MWE0MGItMGU2MC00NzM4LTliYjktNTVjNDc0NmNiNGI0IiwiREkiOiJiYjFlZTFhYy05YzUzLTRmMGYtOGRiYi0zNjVlZGIxYWRlMGQiLCJERCI6MTc3MTEyODgyODF9; STH=4dd02fc4434228baed88fd7d531013851cc776750e5f7cbf15efcefb7db19ab2; gatsby-siteExp=US-NY-SB; bm_sz=0D7318F70EC7F33D715B458891198680~YAAQNZUzuFg49tqCAQAAicnv6xBud4Xy0o4ZJ47nMCLPE5UgqxRQbcGAMturKXWUGUk43OATeCiEa6jOu+YxJg8uvJUPMwzDFSgdF2kKw/QmJBQSn1hn/ZDcmzQ9mPpk3usMUTreqJR6r8L/3CVKDj9j56t97YpuOOUrLXQrc2xZGgf7tlEgzAAylshNXnDs0pqvj8ahy5iLv5AHfDs6wdeKdLiZf4LuYEKjsS6uvM7X4QXSNOQBSO4oqdtTo/LS8iqwUmoQ9IkXZEM4deGWM4vEW7SeEnT9jBUd9B5emnDfKyrOEpDWJ9iUzfeI+1bqZFCfiG2RS0MRy7kz0yvz~4408883~4343345; ak_bmsc=80F4FE5DFFA3D442B8A1A62635C78275~000000000000000000000000000000~YAAQNZUzuBb099qCAQAAcw4/7BDWWOgctvhFbs2hBzjCYOmy1Glo72bfC6cRPr7RCetw2MWe6QUEBR3p8+C5/mv5e2YX5wxhnGVxSoCqBcg0hAT6NcaWYE/O05Fp7JmprEuysEqP/QGZPwg5kt9OXjIt3LmJYIPk0O1Rq+o9eyIqD6edJKpeDfga3sL3u813JIaDe7IEwdlvafaA71nbSoTbRu75Df16RkOHETXAe13HLi39MdEomo1Oapxzavn6QFNLB/lKznw+JzyeZy2sQIGL7OC2nn5HWP2SJH3JM5kRYPnVkSeu+gaMKWItwsISiYS9lAocPVcbC+4fR/rI/rez/xX1wSets/wMoo3OfA0qyJYc6jlXrn+R4kTjScb0j2tvv0rSD6IzqGgt3R0bmhLoGnaTyfrjwUoqampiXFlNs9Jjikcx; _clck=1triak1|1|f4g|0; _dpm_ses.16f4=*; _hjSession_2150570=eyJpZCI6ImE2Mjk0MDdhLWFiY2QtNDQ4Yy05MGNmLTYyYmZmYWQ0YTk1OSIsImNyZWF0ZWQiOjE2NjE4MjE5MjQ2NTgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=1; _ga=GA1.2.77539636.1658367417; ab.storage.sessionId.b543cb99-2762-451f-9b3e-91b2b1538a42=%7B%22g%22%3A%2289c49147-7788-6f6b-d04f-ce5cb006802f%22%2C%22e%22%3A1661826802178%2C%22c%22%3A1661821922568%2C%22l%22%3A1661825002178%7D; _dpm_id.16f4=07a777bf-99c1-4816-abf1-182d170b8bb7.1658367420.16.1661825002.1661807508.40b34951-89c5-4b6f-aeb1-7387ba0c81a7; _uetsid=d0052780271a11eda34b8576440fca7e; _uetvid=9beb7cf0089511eda978bbcaf47efdf4; _clsk=dlld57|1661825003040|25|1|h.clarity.ms/collect; hgg=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aWQiOiIyMDM2MTM4NTgzNiIsImRrZS02MCI6IjI4NSIsImRraC0xMjYiOiI4MzNUZF9ZSiIsImRrZS0xMjYiOiIwIiwiZGtlLTE0NCI6IjQzMSIsImRrZS0xNDkiOiIzMzczIiwiZGtlLTE1MCI6IjU2NyIsImRrZS0xNTEiOiI0NTciLCJka2UtMTUyIjoiNDU4IiwiZGtlLTE1MyI6IjQ1OSIsImRrZS0xNTQiOiI0NjAiLCJka2UtMTU1IjoiNDYxIiwiZGtlLTE1NiI6IjQ2MiIsImRrZS0xNzkiOiI1NjkiLCJka2UtMjA0IjoiNzEwIiwiZGtlLTIxOSI6IjIyNDYiLCJka2gtMjI5IjoiSWxOaEMwNlMiLCJka2UtMjI5IjoiMCIsImRrZS0yMzAiOiI4NTciLCJka2UtMjg4IjoiMTEyOCIsImRrZS0zMDAiOiIxMTg4IiwiZGtlLTMxOCI6IjEyNjEiLCJka2UtMzQ1IjoiMTM1MyIsImRrZS0zNDYiOiIxMzU2IiwiZGtlLTM5NCI6IjE1NTIiLCJka2gtNDA4IjoiWWRhVlJtRFoiLCJka2UtNDA4IjoiMCIsImRrZS00MTYiOiIxNjQ5IiwiZGtlLTQxOCI6IjE2NTEiLCJka2UtNDE5IjoiMTY1MiIsImRrZS00MjAiOiIxNjUzIiwiZGtlLTQyMSI6IjE2NTQiLCJka2UtNDIyIjoiMTY1NSIsImRrZS00MjkiOiIxNzA1IiwiZGtlLTYzNiI6IjI2OTEiLCJka2UtNzAwIjoiMjk5MiIsImRrZS03MzkiOiIzMTQwIiwiZGtlLTc1NyI6IjMyMTIiLCJka2gtNzY4IjoiVVpHYzBySHgiLCJka2UtNzY4IjoiMCIsImRrZS03OTAiOiIzMzQ4IiwiZGtlLTc5NCI6IjMzNjQiLCJka2UtODA0IjoiMzQxMiIsImRrZS04MDYiOiIzNDI2IiwiZGtlLTgwNyI6IjM0MzciLCJka2UtODI0IjoiMzUxMSIsImRrZS04MjUiOiIzNTE0IiwiZGtlLTgzNCI6IjM1NTciLCJka2UtODM2IjoiMzU3MCIsImRrZS04NjUiOiIzNjk1IiwiZGtoLTg5NSI6IjJ6MERZU0MyIiwiZGtlLTg5NSI6IjAiLCJka2UtOTAzIjoiMzg0OCIsImRrZS05MTciOiIzOTEzIiwiZGtlLTkxOCI6IjM5MTciLCJka2UtOTI0IjoiMzk0MiIsImRrZS05MzgiOiI0MDA0IiwiZGtlLTk0NyI6IjQwNDIiLCJka2UtOTc2IjoiNDE3MSIsImRrZS05OTMiOiI0MjQwIiwiZGtoLTEwMDUiOiJkclluaFVFMSIsImRrZS0xMDA1IjoiMCIsImRrZS0xMDA4IjoiNDMwNSIsImRrZS0xMDgxIjoiNDU4NyIsImRrZS0xMTA0IjoiNDY3NiIsImRrZS0xMTI0IjoiNDc2NCIsImRrZS0xMTI1IjoiNDc2NSIsImRrZS0xMTI2IjoiNDc2OCIsImRrZS0xMTI3IjoiNDc3MyIsImRraC0xMTI5IjoiMjhtaGVmb3AiLCJka2UtMTEyOSI6IjAiLCJka2UtMTEzMCI6IjQ3ODQiLCJka2UtMTE1OCI6IjQ5MDYiLCJka2UtMTE1OSI6IjQ5MDgiLCJka2UtMTE3MiI6IjQ5NjQiLCJka2UtMTE3MyI6IjQ5NjciLCJka2UtMTE3NCI6IjQ5NzAiLCJka2UtMTE4NyI6IjUwMTUiLCJka3MtMTE5MSI6IjUwMzkiLCJka2UtMTIxMCI6IjUxMjciLCJka2UtMTIxMSI6IjUxMzkiLCJka2UtMTIxMiI6IjUxNDEiLCJka2UtMTIxMyI6IjUxNDIiLCJka2gtMTIxOSI6IkJ5SFNaWXg2IiwiZGtlLTEyMTkiOiIwIiwiZGtlLTEyMjEiOiI1MTY4IiwiZGtlLTEyMjMiOiI1MTc3IiwiZGtlLTEyMjQiOiI1MTgxIiwiZGtoLTEyMjciOiJ3QmRXbmF6MyIsImRrZS0xMjI3IjoiMCIsImRraC0xMjI4IjoiTDNCek50LVMiLCJka2UtMTIyOCI6IjAiLCJka2gtMTIzMSI6IkczZTczU2FwIiwiZGtlLTEyMzEiOiIwIiwiZGtlLTEyMzIiOiI1MjE4IiwiZGtlLTEyMzMiOiI1MjIxIiwiZGtzLTEyMzQiOiI1MjI0IiwiZGtzLTEyMzciOiI1MjM2IiwiZGtlLTEyMzgiOiI1MjQwIiwiZGtzLTEyNDAiOiI1MjQ3IiwiZGtlLTEyNDIiOiI1MjU4IiwibmJmIjoxNjYxODI1MDI1LCJleHAiOjE2NjE4MjUzMjUsImlhdCI6MTY2MTgyNTAyNSwiaXNzIjoiZGsifQ.QJbJzHACsC4RzilzccXs_eU4oypkGnFm41uq_V3Af1I; _ga_QG8WHJSQMJ=GS1.1.1661821919.19.1.1661825151.0.0.0; STE="2022-08-30T02:35:52.09053Z"; _abck=08C127B41C6047E3A38AF5AC0AF6F2B5~0~YAAQfH8GYNzgV8eCAQAAp3R/7AgW6W0mTYkZRtRsHZHHWomgsLNfqIrM3rQWEn1iPEOoVJdnkZiTsIFQiOxW3SXSeRu3DBAPZ1xZmO8zlWo5KMJEbKX+PdK3k/nnTFjr+edGSXYjgy0auFvbpu1hJ1/k7clq7sywZWwTzHxLcVLkrrtMcsf3sJR//svaYvii07z4+SJKm1MrUXQejVzWmbpHTqbnQV1pLDNvkc2vXB5bf+G7tBT7Uvtb0s+iIImq3ADQnkCYWbWswKi8AGdYsOP0cHSfAoLlT597qT9GmnucssbBqQEq6UUZ14eANnSn03WVumz8GNtuRYytV3h19UMZwfhrsq0tSf5ScwnI3vQ59UsKInBUXfXritxH+iUumvA=~-1~-1~-1; bm_sv=C4C067AFE7F3CF74DD78F57ACDA7BE9F~YAAQfH8GYN3gV8eCAQAAp3R/7BCYtz4oXafZGiKb+aqDKlFtBVocVYyn4nsVZuOn4Yte0WxdrEQPkkUNVyVqOboHp3Zc++xZGUTZ4Gslktbf14tLS+eTVJ174msTKIGm+NwhdZc3Q9TvRs0uQbblZLZWlC572HxRL5T9QDFgl3MUtG7a9R3tNP9Sh5SKhK6oj/OXEQ+Va8lzFJZdQLMwME3NEZOXVstHRwoBoFgfO6hPvBcev34OlGX98W04W6zb5WbSGlcm~1; STE="2022-08-30T02:29:05.679622Z"; STH=88daae768db8fb9e6a405800b36e7a97e29d6887d42a9de70174864fc2959324; STIDN=eyJDIjoxMjIzNTQ4NTIzLCJTIjozNjM0MzE2MTg3NywiU1MiOjM4MzA0MjAyODk0LCJWIjoyMDM5MzY3NjczNSwiTCI6MSwiRSI6IjIwMjItMDgtMzBUMDI6MDU6MDEuODY2NzY2OVoiLCJTRSI6IlVTLURLIiwiVUEiOiJzcjBoRDVURXBGNE1DMVlFdW5zLzZpR2h3em5uOXlvTnVZMkNSTFJSMFpjPSIsIkRLIjoiY2FkN2RkNGUtMzQ1NS00N2YwLTkwNGUtZDJkZjJmN2I1OTExIiwiREkiOiI5YWFjNjY1Ny1jMTIxLTRlNmUtYjA4ZC03ZDk3YjJjYzM0OTEiLCJERCI6MTg0ODI2NDU2Mzl9; _abck=08C127B41C6047E3A38AF5AC0AF6F2B5~-1~YAAQiJs+FxzXVtiCAQAAcjlj7AhTkwmvihlGmmCBG7Nr+LtBDRSoN8dh0WVMuIYx754ImJP/fNam0FLxsi8ePZbF956ZbznVqncpvJcTGet1DIbQti4rurPjEfICMLT0MF7zNOirewIc5DJ8z7xBs1tZKgC0X2dhHbKIgAbyLU//K3FRygixakQffcv8CYgxtADw2SomBla64kUUyFK9YGwZYIh5J798IHVBxbvOaQIk9nef1g7oJbWHjoo4QSDn0PRev1VVSmielWlTKVspNlL9g9+8lEnVyxOHYROI0VnkGZJRLweHeXlwQcSXYr5eLOdYLmtNJS+iOWLVQKG9sLBTcaYatnL/D2ULYOzqwYpJJrO7BmkcULnHz17mJ0vim9vcwhsxGlYlOACoJFlT1DuHcOtSdFcOXa0aBLg=~-1~-1~-1; _csrf=9a233680-b502-417a-a37d-ca0e64218adb; ak_bmsc=63678F2CB9CD0D822552FBBF655540D4~000000000000000000000000000000~YAAQiJs+Fx3XVtiCAQAAcjlj7BBk4QtAyrdMMxgRzE/6vHSybzRvRENgBLlTAczHjIyKLYuihhVW0X0IgW/sIeBgKSLnr/qEdqmX18fwm8809nXy3xyfb8AWRoqGSsiQIGd67k7R/iOMjPUhr1LyQUMstHeVyH1c3AMq+OntPBTtKrhTvA2T0OMLSFx6egSPnSVIVdWV7tFYlb31Bu/15glUEWU0gyybhXsIIprFFyLKnL44bAwrw3Y/ufO4Hc6zoSfHMHTGPTNZ5RTkiAfRRkzqMikrwIHB6rNAbr2yq0ws2k/16EVeTSRaXMOe153jhZSgvVZotWZSziXDwakUG2UDifDodeoHjugwXqoE9tuchZ42+FceN8bYNxYxGM8=; bm_sv=6CFC95F57B262001EC4DFB1412897C4A~YAAQhU/eFwc/nsiCAQAAT0F57BBjTYKucu6AcH1qI4nXk4SPvOz/uDXtZJpRqGOl9DcEWst4PQRAklq6hqYP2QWB+9eMvxl0yZk0X6LlEoqN6HfTW1xw9IzncQ8tFQxj6Og0b09hJcqifTwnG3nQYphx4Lg+P30EQbpVKGcMIamNzk+GmIFU4eWaAD9KgZEgVjNDfvgbQ+DDHIryXdQbUyeU2ARPoVmWFbGVcYLQqAkp0s5j01RxpSq/im+XugEgKvYEUg==~1; bm_sz=E7FF7033AB53F281352D962AD2998D74~YAAQiJs+Fx7XVtiCAQAAcjlj7BBFmZCFsilvOjSbaNbzdQCwrynEkTYlqa+jtaan0eOS97Hcc32jLImi31WlwibTZIjQ2YM9ys5SJGqNBkTPiOQaC+Dkyzsk8K/8luUUFdzHTZUWwPuPDf+X4erJtcht3bmu+P1zxB4FsRqoTZH+ixAForI+0b3JfpD8esPWYq8TYtLFaHvWOc0PgPgjOqT8WP+9rDBvvDktxRkgsBIlXLwqwDDVs+xS3x+TlD3h1jEhw5XoLjqWrZyMSFpvD9c906oYK3YvSEqlBFgmzD5E1tsIBLHH~3486003~3225924; hgg=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2aWQiOiIyMDM5MzY3NjczNSIsImRrZS02MCI6IjI4NSIsImRrZS0xMjYiOiIzNzQiLCJka2UtMTQ0IjoiNDMxIiwiZGtlLTE0OSI6IjMzNzMiLCJka2UtMTUwIjoiNTY3IiwiZGtlLTE1MSI6IjQ1NyIsImRrZS0xNTIiOiI0NTgiLCJka2UtMTUzIjoiNDU5IiwiZGtlLTE1NCI6IjQ2MCIsImRrZS0xNTUiOiI0NjEiLCJka2UtMTU2IjoiNDYyIiwiZGtlLTE3OSI6IjU2OSIsImRrZS0yMDQiOiI3MTAiLCJka2UtMjE5IjoiMjI0NiIsImRraC0yMjkiOiJJbE5oQzA2UyIsImRrZS0yMjkiOiIwIiwiZGtlLTIzMCI6Ijg1NyIsImRrZS0yODgiOiIxMTI4IiwiZGtlLTMwMCI6IjExODgiLCJka2UtMzE4IjoiMTI2MCIsImRrZS0zNDUiOiIxMzUzIiwiZGtlLTM0NiI6IjEzNTYiLCJka2gtMzk0IjoiQ2ZYQWh6ZE8iLCJka2UtMzk0IjoiMCIsImRraC00MDgiOiJZZGFWUm1EWiIsImRrZS00MDgiOiIwIiwiZGtlLTQxNiI6IjE2NDkiLCJka2UtNDE4IjoiMTY1MSIsImRrZS00MTkiOiIxNjUyIiwiZGtlLTQyMCI6IjE2NTMiLCJka2UtNDIxIjoiMTY1NCIsImRrZS00MjIiOiIxNjU1IiwiZGtlLTQyOSI6IjE3MDUiLCJka2UtNjM2IjoiMjY5MSIsImRrZS03MDAiOiIyOTkyIiwiZGtlLTczOSI6IjMxNDAiLCJka2UtNzU3IjoiMzIxMiIsImRraC03NjgiOiJVWkdjMHJIeCIsImRrZS03NjgiOiIwIiwiZGtlLTc5MCI6IjMzNDgiLCJka2UtNzk0IjoiMzM2NCIsImRrZS04MDQiOiIzNDExIiwiZGtlLTgwNiI6IjM0MjUiLCJka2UtODA3IjoiMzQzNyIsImRrZS04MjQiOiIzNTExIiwiZGtlLTgyNSI6IjM1MTQiLCJka2UtODM0IjoiMzU1NyIsImRrZS04MzYiOiIzNTcwIiwiZGtlLTg2NSI6IjM2OTUiLCJka2gtODk1IjoiMnowRFlTQzIiLCJka2UtODk1IjoiMCIsImRrZS05MDMiOiIzODQ4IiwiZGtlLTkxNyI6IjM5MTMiLCJka2UtOTE4IjoiMzkxNyIsImRrZS05MjQiOiIzOTQyIiwiZGtlLTkzOCI6IjQwMDQiLCJka2UtOTQ3IjoiNDA0MiIsImRrZS05NzYiOiI0MTcxIiwiZGtlLTk5MyI6IjQyNDAiLCJka2gtMTAwNSI6ImRyWW5oVUUxIiwiZGtlLTEwMDUiOiIwIiwiZGtlLTEwMDgiOiI0MzA1IiwiZGtlLTEwODEiOiI0NTg3IiwiZGtlLTExMDQiOiI0Njc2IiwiZGtlLTExMjQiOiI0NzY0IiwiZGtlLTExMjUiOiI0NzY1IiwiZGtlLTExMjYiOiI0NzY4IiwiZGtlLTExMjciOiI0NzczIiwiZGtoLTExMjkiOiIyOG1oZWZvcCIsImRrZS0xMTI5IjoiMCIsImRrZS0xMTMwIjoiNDc4NCIsImRrZS0xMTU4IjoiNDkwNiIsImRrZS0xMTU5IjoiNDkwOCIsImRrZS0xMTcyIjoiNDk2NCIsImRrZS0xMTczIjoiNDk2NyIsImRrZS0xMTc0IjoiNDk3MCIsImRrZS0xMTg3IjoiNTAxNSIsImRraC0xMTkxIjoiMXpTX3hlVmMiLCJka3MtMTE5MSI6IjAiLCJka2UtMTIxMCI6IjUxMjciLCJka2gtMTIxMSI6ImVHU0R4czhpIiwiZGtlLTEyMTEiOiIwIiwiZGtlLTEyMTIiOiI1MTQxIiwiZGtlLTEyMTMiOiI1MTQyIiwiZGtoLTEyMTkiOiJCeUhTWll4NiIsImRrZS0xMjE5IjoiMCIsImRraC0xMjIxIjoiMWVrSms0My0iLCJka2UtMTIyMSI6IjAiLCJka2UtMTIyMyI6IjUxNzciLCJka2UtMTIyNCI6IjUxODAiLCJka2gtMTIyNyI6IndCZFduYXozIiwiZGtlLTEyMjciOiIwIiwiZGtoLTEyMjgiOiJMM0J6TnQtUyIsImRrZS0xMjI4IjoiMCIsImRraC0xMjMxIjoiRzNlNzNTYXAiLCJka2UtMTIzMSI6IjAiLCJka2gtMTIzMiI6ImpFci1HTWkzIiwiZGtlLTEyMzIiOiIwIiwiZGtlLTEyMzMiOiI1MjIwIiwiZGtzLTEyMzQiOiI1MjI0IiwiZGtzLTEyMzciOiI1MjM3IiwiZGtlLTEyMzgiOiI1MjQwIiwiZGtzLTEyNDAiOiI1MjQ3IiwiZGtlLTEyNDIiOiI1MjU4IiwibmJmIjoxNjYxODI0NzQ1LCJleHAiOjE2NjE4MjUwNDUsImlhdCI6MTY2MTgyNDc0NSwiaXNzIjoiZGsifQ.Jy43dDGLkp6_Bsd6eUp5eu0l7EdDwoUSqzyM5K9ESFw',
    'origin': 'https://sportsbook.draftkings.com',
    'referer': 'https://sportsbook.draftkings.com/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }


    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

if __name__ == "__main__":
    array_of_group_ids = get_tennis_events_categories()
    event_ids = get_events_from_competition(array_of_group_ids)

    holder = ''
    ans = collections.defaultdict()
    for event_id in event_ids:
        if event_id not in ans: 
            ans[event_id] = {}
        ans[event_id]['url'] = tennis_prefix + event_id
        ans[event_id]['json'] = get_event_data(event_id)
        
        holder = event_id
    
    # print("RESULT")
    # print(ans)

    with open('dk_current_event.json', 'w') as f:
        json.dump(ans, f)