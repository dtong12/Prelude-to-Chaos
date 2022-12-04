from fanduelCurrentEvents import *
from decimal import Decimal
import json
from datetime import timedelta
import re


class GameLine:
    def __init__(self, line_name, cleaned_line_name, curr_set, curr_game, curr_points, total_points_in_match, total_games_in_match):
        try:
            self.line_name = line_name
            self.cleaned_line_name = cleaned_line_name
            self.curr_set = int(curr_set) if curr_set else curr_set
            self.curr_game = int(curr_game) if curr_game else curr_game
            self.curr_points = int(curr_points) if curr_points else curr_points
            self.total_points_in_match = total_points_in_match
            self.total_games_in_match = total_games_in_match
        except Exception as e:
            # print(traceback.format_exc())
            print(e, "inputs -> ",  line_name, cleaned_line_name, curr_set, curr_game, curr_points, total_points_in_match, total_games_in_match)

class FanduelGameState:
    def __init__(self, event_json):
        #self.event_name =  self.clean_event_name(list(event_json['json']['attachments']['events'].values())[0]['name'])
        try:
            self.event_name = self.clean_event_name(list(event_json['json']['attachments']['events'].values())[0]['name'])
            self.event_json = event_json
            self.game_lines = {}
            self.get_game_lines()
        except Exception as e:
            print("error creating fanduel game state", e)
    
    def clean_event_name(self, event_name):
        mod_event_name = event_name.replace(" v ", " vs ")
        json = self.fanduel_event_name_clean(mod_event_name)
        return json
    
    def fanduel_market_clean_remove_first_name(self, fanduel_line):
        fanduel_line = fanduel_line.strip()
        if '/' not in fanduel_line and " " in fanduel_line: #if there is no / and there is a space
            last_name = fanduel_line[fanduel_line.rindex(" "):]
            return last_name.strip()
        else:
            return fanduel_line.strip()

    def fanduel_event_name_clean(self, fanduel_line):
        #doubles
        fanduel_line.strip()
        if '/' in fanduel_line: 
            fanduel_vs_split = fanduel_line.split("vs")

            team_one, team_two = fanduel_vs_split[0], fanduel_vs_split[1]

            team_one_player_one , team_one_player_two = team_one.split("/")[0], team_one.split("/")[1]
            team_two_player_one, team_two_player_two = team_two.split("/")[0], team_two.split("/")[1]
            
            team_one_player_one = self.fanduel_market_clean_remove_first_name(team_one_player_one)
            team_one_player_two = self.fanduel_market_clean_remove_first_name(team_one_player_two)
            team_two_player_one = self.fanduel_market_clean_remove_first_name(team_two_player_one)
            team_two_player_two = self.fanduel_market_clean_remove_first_name(team_two_player_two)
            ans = team_one_player_one + '/' + team_one_player_two + " vs " + team_two_player_one + "/" + team_two_player_two
            return ans

        #singles
        elif '/' not in fanduel_line:
            fanduel_vs_split = fanduel_line.split("vs")

            player_one, player_two = fanduel_vs_split[0].strip(), fanduel_vs_split[1].strip()
            player_one = self.fanduel_market_clean_remove_first_name(player_one)
            player_two = self.fanduel_market_clean_remove_first_name(player_two)
        
            ans = player_one + " vs "+ player_two
            return ans

    def strip_game_line(self, game_line):
        game_line = game_line.replace("-", "").replace("/", "")
        return([i for i in re.sub(r'[.,!?]', '', game_line.lower()).split() if not re.search(r'\d', i)])

    def get_game_lines(self):
        # event_json = self.event_json['json']['attachments']['markets']
        markets = self.event_json['json']['attachments']['markets']
        for market_key in markets:
            #print(markets[market_key]['marketName'])
            fanduel_stripped_line_name = self.strip_game_line(markets[market_key]['marketName'])

            if markets[market_key]['inPlay'] == True and markets[market_key]['marketStatus'] == 'OPEN': #added line
                if fanduel_stripped_line_name == ['set', 'game', 'winner']:
                    self.game_lines[markets[market_key]['marketName']] = self.set_game_winner(markets[market_key]['marketName'])
                elif fanduel_stripped_line_name == ['total', 'match', 'games']:
                    self.game_lines[markets[market_key]['marketName']] = self.total_match_games(markets[market_key]['marketName'])
                elif fanduel_stripped_line_name == ['set', 'game', 'handicap']:
                    self.game_lines[markets[market_key]['marketName']] = self.set_game_handicap(markets[market_key]['marketName'])
                elif fanduel_stripped_line_name == ['correct', 'score', 'set']:
                    self.game_lines[markets[market_key]['marketName']] = self.correct_score_set(markets[market_key]['marketName'])
                elif fanduel_stripped_line_name == ['set', 'game', 'point', 'winner']:
                    self.game_lines[markets[market_key]['marketName']] = self.set_game_point_winner(markets[market_key]['marketName'])
                elif fanduel_stripped_line_name == ['set', 'winner']:
                    self.game_lines[markets[market_key]['marketName']] = self.set_winner(markets[market_key]['marketName']) 
                elif fanduel_stripped_line_name == ['set', 'total', 'games', 'overunder']:
                    self.game_lines[markets[market_key]['marketName']] = self.set_total_games_overunder(markets[market_key]['marketName']) 
                else:
                    print("remaining -> ", self.strip_game_line(markets[market_key]['marketName']), markets[market_key]['marketName'])
                    pass

    def set_game_winner(self, fanduel_raw_name):
        partial_cleaned_fanduel_name = fanduel_raw_name.replace("|", "").replace("-", "")
        cleaned_fanduel_name_array = fanduel_raw_name.replace("|", "").replace("-", "").split()
        curr_set = cleaned_fanduel_name_array[1]
        curr_game = cleaned_fanduel_name_array[3]
        return GameLine(line_name = partial_cleaned_fanduel_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def total_match_games(self, fanduel_raw_name):
        partial_cleaned_fanduel_name = fanduel_raw_name.replace("|", "").replace("-", "")
        cleaned_fanduel_name_array = fanduel_raw_name.replace("|", "").replace("-", "").split()
        total_games_in_match = cleaned_fanduel_name_array[3]
        return GameLine(line_name = partial_cleaned_fanduel_name, cleaned_line_name= None, curr_set= None, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= total_games_in_match) 

    def set_game_handicap(self, fanduel_raw_name):
        partial_cleaned_fanduel_name = fanduel_raw_name.replace("|", "").replace("-", "")
        cleaned_fanduel_name_array = fanduel_raw_name.replace("|", "").replace("-", "").split()
        curr_set = cleaned_fanduel_name_array[1]
        return GameLine(line_name = partial_cleaned_fanduel_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def correct_score_set(self, fanduel_raw_name):
        partial_cleaned_fanduel_name = fanduel_raw_name.replace("|", "").replace("-", "")
        cleaned_fanduel_name_array = fanduel_raw_name.replace("|", "").replace("-", "").split()
        curr_set = cleaned_fanduel_name_array[2][0]
        return GameLine(line_name = partial_cleaned_fanduel_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def set_game_point_winner(self, fanduel_raw_name):
        partial_cleaned_fanduel_name = fanduel_raw_name.replace("|", "").replace("-", "")
        cleaned_fanduel_name_array = fanduel_raw_name.replace("|", "").replace("-", "").split()
        curr_set = cleaned_fanduel_name_array[1][0]
        curr_game = cleaned_fanduel_name_array[3]
        point_in_game = cleaned_fanduel_name_array[5]
        return GameLine(line_name = partial_cleaned_fanduel_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = point_in_game, total_points_in_match= None, total_games_in_match= None) 

    def set_winner(self, fanduel_raw_name):
        partial_cleaned_fanduel_name = fanduel_raw_name.replace("|", "").replace("-", "")
        cleaned_fanduel_name_array = fanduel_raw_name.replace("|", "").replace("-", "").split()
        curr_set = cleaned_fanduel_name_array[1][0]
        return GameLine(line_name = partial_cleaned_fanduel_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 
    
    def set_total_games_overunder(self, fanduel_raw_name):
        partial_cleaned_fanduel_name = fanduel_raw_name.replace("|", "").replace("-", "")
        cleaned_fanduel_name_array = fanduel_raw_name.replace("|", "").replace("-", "").split()
        curr_set = cleaned_fanduel_name_array[1][0]
        return GameLine(line_name = partial_cleaned_fanduel_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 


def test_full_code(type):
    ans = collections.defaultdict()
    if type == 'local':
        print("test local beginning")
        json_res = json.load(open('fd_current_event.json'))
        timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    elif type == 'online':
        res = async_fanduel_main() #fanduel_main()
        timestamp, json_res = res['timestamp'], res['ans']
    count = 0

    print("number of games", len(json_res))

    for test_event in json_res:
        try:
            ingested_fanduel = FanduelGameState(json_res[test_event])
            ans[ingested_fanduel.event_name] = ingested_fanduel
            count += 1 
        except:
            pass
    return ans



if __name__ == "__main__":
    # res = test_full_code('local')
    res = test_full_code('online')