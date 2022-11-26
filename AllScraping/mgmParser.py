from mgmCurrentEvents import *
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


class MgmGameState: 
    def __init__(self, event_json):
        try:
            self.event_name = clean_event_name(event_json['json']['fixture']['participants'])
            print("EVENT NAME", self.event_name)
            self.event_json = event_json
            self.game_lines = {}
            self.get_game_lines()
        except Exception as e:
            print('mgm : error getting event name')
            exit
    
    def get_game_lines(self):
        markets = self.event_json['json']['fixture']['games']
        for market in markets:
            mgm_stripped_line_name = self.strip_line_name(market['name']['value'])

            if market['visibility'] == 'Visible':
                if mgm_stripped_line_name == ['set','winner']:
                    self.game_lines[market['name']['value']] = self.set_winner(market['name']['value'])
                elif mgm_stripped_line_name == ['game', 'to', 'deuce', 'set']:
                    self.game_lines[market['name']['value']] = self.game_to_deuce_set(market['name']['value'])
                elif mgm_stripped_line_name == ['correct', 'score', 'set', 'game']:
                    self.game_lines[market['name']['value']] = self.correct_score_set_game(market['name']['value'])
                elif mgm_stripped_line_name == ['game', 'winner', 'set']:
                    self.game_lines[market['name']['value']] = self.game_winner_set(market['name']['value']) 
                elif mgm_stripped_line_name == ['point', 'winner', 'game', 'set']:
                    self.game_lines[market['name']['value']] = self.point_winner_game_set(market['name']['value']) 
                elif mgm_stripped_line_name == ['total', 'games', 'set']:
                    self.game_lines[market['name']['value']] = self.total_games_set(market['name']['value']) 
                elif mgm_stripped_line_name == ['game', 'total', 'points', 'set']:
                    self.game_lines[market['name']['value']] = self.game_total_points_set(market['name']['value'])     
                elif mgm_stripped_line_name == ['tiebreak', 'in', 'set']:
                    self.game_lines[market['name']['value']] = self.tiebreak_in_set(market['name']['value'])     
                elif mgm_stripped_line_name == ['correct', 'score', 'set']:
                    self.game_lines[market['name']['value']] = self.correct_score_set(market['name']['value'])     
                elif mgm_stripped_line_name == ['game', 'after', 'points', 'set']:
                    self.game_lines[market['name']['value']] = self.game_after_points_set(market['name']['value'])     
                elif mgm_stripped_line_name == ['set', 'score', 'after', 'games']:
                    self.game_lines[market['name']['value']] = self.set_score_after_games(market['name']['value'])     
                elif mgm_stripped_line_name == ['game', '+', 'winner', 'set']:
                    self.game_lines[market['name']['value']] = self.game_plus_winner_set(market['name']['value'])     
                elif mgm_stripped_line_name == ['correct', 'score', 'group', 'set', 'game']:
                    self.game_lines[market['name']['value']] = self.correct_score_group_set_game(market['name']['value'])     
                elif mgm_stripped_line_name == ['who', 'will', 'win', 'more', 'games', 'in', 'the', 'set', 'player', 'spread']:
                    self.game_lines[market['name']['value']] = self.who_will_win_more_games_in_the_set_player_spread(market['name']['value'])     
                elif mgm_stripped_line_name == ['point', 'winner', 'tiebreak', 'set']:
                    self.game_lines[market['name']['value']] = self.point_winner_tiebreak_set(market['name']['value'])     
                elif mgm_stripped_line_name == ['how', 'many', 'points', 'will', 'there', 'be', 'in', 'the', 'set', 'tiebreak']:
                    self.game_lines[market['name']['value']] = self.how_many_points_will_there_be_in_the_set_tiebreak(market['name']['value'])     
                elif set(['how', 'many', 'games', 'will', 'player', 'win', 'in', 'the', 'set']).issubset(set(mgm_stripped_line_name)):
                    self.game_lines[market['name']['value']] = self.how_many_games_will_player_win_in_the_set(market['name']['value'])     
                else: 
                    if 'race' not in mgm_stripped_line_name and mgm_stripped_line_name != ['how', 'many', 'games', 'will', 'player', 'win', 'in', 'the', 'match'] and mgm_stripped_line_name != ['player', 'to', 'win', 'at', 'least', 'set']: 
                        print("remaining -> ",mgm_stripped_line_name, "->" , market['name']['value'])
    def how_many_points_will_there_be_in_the_set_tiebreak(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        curr_set = cleaned_mgm_name_array[8][1]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 
 
    def point_winner_tiebreak_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split() 
        curr_set = cleaned_mgm_name_array[5]
        point_in_game = cleaned_mgm_name_array[1]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = point_in_game, total_points_in_match= None, total_games_in_match= None) 
    
    def set_winner(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        #print("set winner cleaned *************", cleaned_mgm_name_array)
        curr_set = cleaned_mgm_name_array[1]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def game_to_deuce_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        curr_game = cleaned_mgm_name_array[1]
        curr_set = cleaned_mgm_name_array[5]
        # print("game to deuce *******", cleaned_mgm_name_array, curr_set, curr_game)
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def correct_score_set_game(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        curr_set = cleaned_mgm_name_array[3]
        curr_game = cleaned_mgm_name_array[5]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def game_winner_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        curr_game = cleaned_mgm_name_array[1]
        curr_set = cleaned_mgm_name_array[4]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def point_winner_game_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        curr_set = cleaned_mgm_name_array[6]
        curr_game = cleaned_mgm_name_array[4]
        point_in_game = cleaned_mgm_name_array[1]
        #print("POINT WINNTER GAME SET", cleaned_mgm_name_array, curr_set, curr_game, point_in_game)
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = point_in_game, total_points_in_match= None, total_games_in_match= None) 

    def total_games_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        curr_set = cleaned_mgm_name_array[3]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def game_total_points_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        curr_set = cleaned_mgm_name_array[5]
        curr_game = cleaned_mgm_name_array[1]
        #print("GAME TOTAL POINTS", cleaned_mgm_name_array, curr_set, curr_game)
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None) 
 
    def tiebreak_in_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        #print('TIE BREAK IN SET', cleaned_mgm_name_array)
        curr_set = cleaned_mgm_name_array[3]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def correct_score_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        #print("correct score set", cleaned_mgm_name_array)
        curr_set = cleaned_mgm_name_array[3]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def game_after_points_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        #print("game_after_points_set", cleaned_mgm_name_array)
        curr_set = cleaned_mgm_name_array[6]
        curr_game = cleaned_mgm_name_array[1]
        point_in_game = cleaned_mgm_name_array[3]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = point_in_game, total_points_in_match= None, total_games_in_match= None) 

    def set_score_after_games(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        #print("set_score_after_games", cleaned_mgm_name_array)
        curr_set = cleaned_mgm_name_array[1]
        curr_game = cleaned_mgm_name_array[4]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def game_plus_winner_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        #print("game plus winner set", cleaned_mgm_name_array)
        curr_set = cleaned_mgm_name_array[6]
        curr_game = cleaned_mgm_name_array[3]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def correct_score_group_set_game(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        #print("CORRECT SCORE GROUP TEST?", cleaned_mgm_name_array)
        curr_set = cleaned_mgm_name_array[4]
        curr_game = cleaned_mgm_name_array[6]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def how_many_games_will_player_win_in_the_set(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        set_time = cleaned_mgm_name_array[9]
        curr_set = 100
        if set_time == 'first': 
            curr_set = 1
        elif set_time == 'second':
            curr_set = 2
        else:
            curr_set = 3
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 

    def who_will_win_more_games_in_the_set_player_spread(self, mgm_raw_name):
        partial_cleaned_mgm_name = mgm_raw_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        cleaned_mgm_name_array = partial_cleaned_mgm_name.split()
        #print('who_will_win_more_games_in_the_set_player_spread', cleaned_mgm_name_array)
        curr_set = cleaned_mgm_name_array[7][0]
        return GameLine(line_name = partial_cleaned_mgm_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None) 


    def strip_line_name(self, market_name):
        inter = market_name.lower().replace(",", "").replace("-","").replace("  ", " ").replace("(", "").replace(")", "")
        return([i for i in re.sub(r'[.,!?]', '', inter.lower()).split() if not re.search(r'\d', i)])

def clean_event_name(participants): #put in participants

    def single_event_clean_first_name(participant_name):
        player_name_array = participant_name.split()
        return player_name_array[-1]
    
    def doubles_event_clean_first_name(participant_name):
        split_by_slash = participant_name.split("/")
        #print("split by slash", split_by_slash)
        player_one = split_by_slash[0]
        player_two = split_by_slash[1]

        cleaned_player_one = single_event_clean_first_name(player_one)
        cleaned_player_two = single_event_clean_first_name(player_two)
        return f"{cleaned_player_one}/{cleaned_player_two}"

    participant_a = participants[0]['name']['short']
    participant_b = participants[1]['name']['short']

    if "/" in participant_a and "/" in participant_b:
        cleaned_participant_a = doubles_event_clean_first_name(participant_a)
        cleaned_participant_b = doubles_event_clean_first_name(participant_b)
    else:
        cleaned_participant_a = single_event_clean_first_name(participant_a)
        cleaned_participant_b = single_event_clean_first_name(participant_b)

    ans = f"{cleaned_participant_a} vs {cleaned_participant_b}"
    return ans


def test_full_code(type):
    ans = collections.defaultdict()
    if type == 'local':
        print("test local beginning")
        json_res = json.load(open('mgm_current_event.json'))
        timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    elif type == 'online':
        res = async_mgm_main() #fanduel_main()
        timestamp, json_res = res['timestamp'], res['ans']
    count = 0

    print("mgm: number of games", len(json_res))
    for test_event in json_res:
        try:
            ingested_fanduel = MgmGameState(json_res[test_event])
            ans[ingested_fanduel.event_name] = ingested_fanduel
            count += 1 
        except:
            pass
    return ans

if __name__ == "__main__":
    res = test_full_code("online")