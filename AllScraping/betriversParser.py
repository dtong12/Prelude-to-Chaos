from betriversCurrentEvents import *
import json
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
            print(e, "inputs -> ",  line_name, cleaned_line_name, curr_set, curr_game, curr_points, total_points_in_match, total_games_in_match)


class BetriversGameState:
    def __init__(self, event_json):
        try:
            self.event_name = self.clean_event_name(event_json)
            self.event_json = event_json
            self.game_lines = {}
            self.get_game_lines()
        except Exception as e:
            print("error creating betrivers game state", e)
    
    def clean_event_name(self, event_json):
        home_name = event_json['json']['events'][0]['homeName']
        away_name = event_json['json']['events'][0]['awayName']
        
        player_one = self.get_first_name(home_name)
        player_two = self.get_first_name(away_name)
        ans = f"{player_one} vs {player_two}"
        return ans

    def get_first_name(self, participant_name):        
        if "/" in participant_name:
            slash_split = participant_name.split("/")
            first_player = slash_split[0]
            second_player = slash_split[1]
            first_player_first_name_comma_split = first_player.split(",")
            second_player_first_name_comma_split = second_player.split(",")

            first_name_player_one = first_player_first_name_comma_split[0].split(" ")[-1]
            first_name_player_two = second_player_first_name_comma_split[0].split(" ")[-1]
            ans = f"{first_name_player_one}/{first_name_player_two}"

            return f"{first_name_player_one}/{first_name_player_two}"
        else:
            comma_split = participant_name.split(",")
            first_element = comma_split[0]
            first_name = first_element.split()[-1]
            return first_name
    
    def strip_game_line(self, game_line):
        game_line = game_line.replace("-", "").replace("/", "")
        return([i for i in re.sub(r'[.,!?]', '', game_line.lower()).split() if not re.search(r'\d', i)])
    
    def get_game_lines(self):
        bet_offers = self.event_json['json']['betOffers']
        for bet_offer in bet_offers:
            if bet_offer['outcomes'][0]['status'] == 'OPEN':
                betrivers_stripped_line_name = self.strip_game_line(bet_offer['criterion']['label'])
                partial_cleaned_betrivers_name = bet_offer['criterion']['label'].replace("|", "").replace("-", "")
                cleaned_betrivers_name_array = bet_offer['criterion']['label'].replace("|", "").replace("-", "").replace(",", "").split()

                if betrivers_stripped_line_name == ['set']:
                    self.game_lines[bet_offer['criterion']['label']] = self.set_winner(partial_cleaned_betrivers_name, cleaned_betrivers_name_array)
                elif betrivers_stripped_line_name == ['first', 'to', 'games', 'set']:
                    self.game_lines[bet_offer['criterion']['label']] = self.first_to_games_set(partial_cleaned_betrivers_name, cleaned_betrivers_name_array)
                elif betrivers_stripped_line_name == ['correct', 'score', 'set', 'game']:
                    self.game_lines[bet_offer['criterion']['label']] = self.correct_score_set_game(partial_cleaned_betrivers_name, cleaned_betrivers_name_array)
                elif betrivers_stripped_line_name == ['set', 'game']:
                    self.game_lines[bet_offer['criterion']['label']] = self.set_game(partial_cleaned_betrivers_name, cleaned_betrivers_name_array)
                elif betrivers_stripped_line_name == ['point', 'set', 'game']:
                    self.game_lines[bet_offer['criterion']['label']] = self.point_set_game(partial_cleaned_betrivers_name, cleaned_betrivers_name_array)
                elif betrivers_stripped_line_name == ['deuce', 'in', 'set', 'game']:
                    self.game_lines[bet_offer['criterion']['label']] = self.deuce_in_set_game(partial_cleaned_betrivers_name, cleaned_betrivers_name_array)
                elif betrivers_stripped_line_name == ['tie', 'break', 'in', 'set']:
                    self.game_lines[bet_offer['criterion']['label']] = self.tie_break_in_set(partial_cleaned_betrivers_name, cleaned_betrivers_name_array)
                elif betrivers_stripped_line_name == ['tiebreak', 'total', 'Points', 'set']:
                    self.game_lines[bet_offer['criterion']['label']] = self.tiebreak_total_points_set(partial_cleaned_betrivers_name, cleaned_betrivers_name_array)
                else:
                    print('remaining -> ', betrivers_stripped_line_name,  "  --  ", cleaned_betrivers_name_array)
                # else:
                #     print("remaining lines ->", partial_cleaned_betrivers_name, cleaned_betrivers_name_array)    

    def set_winner(self, partial_cleaned_name, cleaned_fanduel_name_array):
        curr_set = cleaned_fanduel_name_array[1]
        return GameLine(line_name = partial_cleaned_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 
    def first_to_games_set(self, partial_cleaned_name, cleaned_fanduel_name_array):
        curr_set = cleaned_fanduel_name_array[5]
        return GameLine(line_name = partial_cleaned_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 
    def correct_score_set_game(self, partial_cleaned_name, cleaned_fanduel_name_array):
        curr_set = cleaned_fanduel_name_array[3]
        curr_game = cleaned_fanduel_name_array[5]
        return GameLine(line_name = partial_cleaned_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None) 
    def set_game(self, partial_cleaned_name, cleaned_fanduel_name_array):
        curr_set = cleaned_fanduel_name_array[1]
        curr_game = cleaned_fanduel_name_array[3]
        return GameLine(line_name = partial_cleaned_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None) 
    def point_set_game(self, partial_cleaned_name, cleaned_fanduel_name_array):
        curr_set = cleaned_fanduel_name_array[3]
        curr_game = cleaned_fanduel_name_array[5]
        point_in_game = cleaned_fanduel_name_array[1]
        return GameLine(line_name = partial_cleaned_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = point_in_game, total_points_in_match= None, total_games_in_match= None) 
    def deuce_in_set_game(self, partial_cleaned_name, cleaned_fanduel_name_array):
        curr_set = cleaned_fanduel_name_array[3]
        curr_game = cleaned_fanduel_name_array[5]
        return GameLine(line_name = partial_cleaned_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points =  None, total_points_in_match= None, total_games_in_match= None) 
    def tie_break_in_set(self, partial_cleaned_name, cleaned_fanduel_name_array):
        curr_set = cleaned_fanduel_name_array[4]
        return GameLine(line_name = partial_cleaned_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 
    def tiebreak_total_points_set(self, partial_cleaned_name, cleaned_fanduel_name_array):
        curr_set = cleaned_fanduel_name_array[4]
        return GameLine(line_name = partial_cleaned_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 


def test_full_code(type):
    ans = collections.defaultdict()
    if type == 'local':
        print("test local beginning")
        json_res = json.load(open('br_current_event.json'))
        timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    elif type == 'online':
        res = async_betrivers_main() #betrivers_main()
        timestamp, json_res = res['timestamp'], res['ans']
    count = 0

    print("number of games", len(json_res))
    for test_event in json_res:
        try:
            ingested_betrivers = BetriversGameState(json_res[test_event])
            ans[ingested_betrivers.event_name] = ingested_betrivers
            count += 1 
        except:
            pass
    return ans

if __name__ == "__main__":
    res = test_full_code('online')
