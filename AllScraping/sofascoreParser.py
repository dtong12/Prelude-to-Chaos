from sofascoreCurrentEvents import *
from unidecode import unidecode



#https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp


def test_local():
    test = json.load(open('softscore_current_event.json'))
    
    print(test.keys())
    for event in test:
        try:
            home_team_name = unidecode(test[event]['game_data_json']['event']['homeTeam']['shortName'])
            away_team_name = unidecode(test[event]['game_data_json']['event']['awayTeam']['shortName'])
            
            home_team_name = clean_event_name(home_team_name)
            away_team_name = clean_event_name(away_team_name)

            ans = f"{home_team_name} vs {away_team_name}"
            print("combined event", home_team_name, away_team_name)

        except Exception as e:
            print('error occured', e)

def clean_event_name(team_name):
    
    team_name = team_name.replace(".", " ")
    team_name = ' '.join( [w for w in team_name.split() if len(w)>1 or w == "/"] )#.replace(" ", "")
    # print(team_name)
    
    if "/" in team_name:
        index_slash = 0
        for index in range(len(team_name.split())):
            if team_name.split()[index] == '/':
                first_player_name = team_name.split()[0:index_slash+1][-1]
                second_player_name = team_name.split()[index_slash+1:][-1]
                # print(len(first_player_name))
                # print("first player name", first_player_name)
                #print("names first and second ", first_player_name, second_player_name)
        #print("one doubles team -> ", f"{first_player_name}/{second_player_name}")
        return f"{first_player_name}/{second_player_name}"

    # if " " in team_name: print("split", team_name.split())
    #if " " in team_name: team_name = team_name.split()[-1] #edge case HA Minh Duc VU vs Fuele

    # print("    intermediate home", home_team_name)
    # print("    intermediate away", away_team_name)
    # print("single team name", team_name)

    ans = team_name.split()[-1] #THIS accounts for middle names like "Jimenez Kasintseva V.""
    return ans


def get_event_name(event):
    home_team_name = unidecode(event['game_data_json']['event']['homeTeam']['shortName'])
    away_team_name = unidecode(event['game_data_json']['event']['awayTeam']['shortName'])
    home_team_name = clean_event_name(home_team_name)
    away_team_name = clean_event_name(away_team_name)

    # print("combined event", home_team_name, away_team_name)
    ans = f"{home_team_name} vs {away_team_name}"
    return ans

def ingest_softscore_data():

    all_event_json = json.load(open('softscore_current_event.json'))
    res = collections.defaultdict()
    for event in all_event_json:
        #uprint(all_event_json[event])
        event_json = all_event_json[event]
        ingested_sofascore = SofaScoreGameState(event_json)
        res[ingested_sofascore.event_name] = ingested_sofascore
        pretty_print = vars(ingested_sofascore)
        for thing in pretty_print:
            try:
                if thing != 'input': print(thing, pretty_print[thing])
            except Exception as e:
                print(e)
            pass
        print()
    return res


#remainining features that don't exist yet
#total points per game #Set 3 - Game 5 Total Points
#total points per set


class SofaScoreGameState:
    def __init__(self, event_json):

        self.event_name = get_event_name(event_json)

        self.curr_state = ''
        self.curr_set = '' #set 2
        self.curr_game = '' #game 8
        self.curr_points = '' #11th point
        self.home_player = '' #arasaka
        self.away_player = '' #david
        self.total_points_in_match = '' #45.5 o/u points
        self.total_games_in_match = '' #15 o/u games
        self.input = event_json
        self.curr_state_init()

    def curr_state_init(self):
        try: self.curr_state = self.input['game_data_json']['event']['status']['type']
        except: self.curr_state = None
        try: self.curr_set = int(self.input['game_data_json']['event']['status']['description'][0]) #"3rd set" just take the first character
        except: self.curr_set = None
        try: #reading just the length doesn't work because when the set changes.. the set changes, but the games dont update till the first one is done (first one is done == first point is scored?)
            #hence caesars reads set 2, game 1, but sofa reads set 2 (but the games are still from set 1 so the length is 10)
            #fixed this by reading for specific set
            self.curr_game = 1

            if len(self.input['point_by_point']['pointByPoint']) == 0:
                print("Notes: No point by point data")
                raise Exception
            for specific_set in self.input['point_by_point']['pointByPoint']:
                # print("specific_set", specific_set)
                if specific_set['set'] == self.curr_set:
                    # print("specific_set", specific_set[0]['games'])
                    # print("specific set", specific_set)
                    self.curr_game = len(specific_set['games']) 
        except: 
            self.curr_game = None #should be the current games for the current set
        try:   
            #implement something similar to the one above
            # We need to make sure that game array we are reading points from is the latest game of the new set.
            #Ex: Sofascore should read set 2, game 1, point 1
            #but instead it reads set 2, game 1, point 10 (10 points in set 1, game 7, point 10)
            
            #so we must read it as follows

            self.curr_points = 1 #default of 1

            if len(self.input['point_by_point']['pointByPoint']) == 0:
                print("Notes: No point by point data in curr_points scan")
                raise Exception
            
            for specific_set in self.input['point_by_point']['pointByPoint']:
                # print("specific_set", specific_set)
                if specific_set['set'] == self.curr_set:

                    self.curr_points = len(specific_set['games'][0]['points'])#len(specific_set['games']) 

            #old code below
            #self.curr_points = len(self.input['point_by_point']['pointByPoint'][0]['games'][0]['points']) #this is just taking the top games open Edit: This leads to errors due to when a new set opens, 
        except: 
            self.curr_points = None

        try: self.home_player = self.input['game_data_json']['event']['homeTeam']['shortName']
        except: self.home_player = None
        try: self.away_player = self.input['game_data_json']['event']['awayTeam']['shortName']
        except: self.away_player = None
        try: 
            game_statistics = self.input['game_statistics']['statistics'][0]['groups']
            for group in game_statistics:
                if group['groupName'] == 'Points':
                    statisticsItems = group['statisticsItems']
                    for statisticsItem in group['statisticsItems']:
                        if statisticsItem['name'] == 'Total points won':
                            home = int(statisticsItem['home'])
                            away = int(statisticsItem['away'])
                            self.total_points_in_match = home + away
                            pass
        except Exception as e:
            print("Could not get total points", e)
            self.total_points_in_match = None
        try:
            game_statistics = self.input['game_statistics']['statistics'][0]['groups']
            for group in game_statistics:
                if group['groupName'] == 'Other':                    
                    statisticsItem = group['statisticsItems']
                    for statisticsItem in group['statisticsItems']:
                        if statisticsItem['name'] == 'Games won':
                            home = int(statisticsItem['home'])
                            away = int(statisticsItem['away'])
                            self.total_games_in_match = home + away
        except Exception as e:
            print("error -> ", e)
            self.total_games_in_match = None




if __name__ == "__main__":
    #test_local()
    #store something else on top
    # test_local()
    #sofascore_main()
    async_sofascore_main()
    ingest_softscore_data()