from draftkingsCurrentEvents import *
from decimal import Decimal
import json
from datetime import timedelta
import re
import traceback



"""
{frozenset({'set', 'total', 'games'}), frozenset({'total', 'games'}), frozenset({'score', 'set', 'game', 'correct'}), frozenset({'total', 'sets'}), frozenset({'total', 'set', 'game', 'points'}), frozenset({'score', 'correct'}), frozenset({'set', 'game', 'winner'}), frozenset({'at', 'least', 'player', 'to', 'win', 'set', 'one'}), frozenset({'score', 'set', 'correct'}), frozenset({'point', 'set', 'game', 'winner'}), frozenset({'moneyline', 'set'}), frozenset({'spread', 'games'}), frozenset({'deuce', 'set', 'game', 'to'}), frozenset({'any', 'set', 'finish', 'to'}), frozenset({'after', 'score', 'set', 'games'}), frozenset({'race', 'set', 'to', 'games'}), frozenset({'set'}), frozenset({'moneyline'})}
"""

class GameLine:
    def __init__(self, line_name, cleaned_line_name, curr_set, curr_game, curr_points, total_points_in_match, total_games_in_match):
        try:
            self.line_name = line_name
            self.cleaned_line_name = cleaned_line_name
            self.curr_set = int(curr_set) if curr_set else curr_set
            self.curr_game = int(curr_game) if curr_game else curr_game
            self.curr_points = curr_points
            self.total_points_in_match = total_points_in_match
            self.total_games_in_match = total_games_in_match
        except Exception as e:
            # print(traceback.format_exc())
            print(e, "inputs -> ",  line_name, cleaned_line_name, curr_set, curr_game, curr_points, total_points_in_match, total_games_in_match)


class DraftkingsGameState:
    def __init__(self, event_json):
        self.event_name = clean_event_name(event_json['json']['event']['name'])
        self.event_json = event_json
        self.game_lines = {}
        self.get_game_lines()

    def strip_game_line(self, game_line):
        game_line = game_line.replace("-", "").replace("/", "")
        return([i for i in re.sub(r'[.,!?]', '', game_line.lower()).split() if not re.search(r'\d', i)])

    def get_game_lines(self):
        print('event name ->',self.event_name)
        # print("number of lines to read -> ", len(self.event_json['json']['markets']))
        #input all of them as gamelines

        # print(self.event_json['json']['eventCategories'].keys())
        unique_lines = set()
        for eventCategory in self.event_json['json']['eventCategories']:
            componentizedOffers = eventCategory['componentizedOffers']
            for offer in componentizedOffers:
                    for bottom_offer in offer['offers'][0]: #this doesn't read specific lines, just the overall category
                        #this is good enough for most lines, only fails for "total games -listed set" and similar ones
                        draftkings_cleaned_name = self.strip_game_line(bottom_offer['label'])
                        #print("raw ->", bottom_offer['label'])

                        if bottom_offer['isOpen'] == True and bottom_offer['isSuspended'] == False:
                            if draftkings_cleaned_name == ['set', 'game', 'point', 'winner']:
                                self.game_lines[bottom_offer['label']] = self.set_game_point_winner(bottom_offer['label'])
                            elif draftkings_cleaned_name == ['set', 'game', 'winner']:
                                self.game_lines[bottom_offer['label']] = self.set_game_winner(bottom_offer['label'])
                            elif draftkings_cleaned_name == ['set']:
                                self.game_lines[bottom_offer['label']] = self._set_(bottom_offer['label'])
                            # elif draftkings_cleaned_name == ['total', 'games']:
                            #     self.game_lines[bottom_offer['label']] = self.total_games(bottom_offer['outcomes'])
                            elif draftkings_cleaned_name == ['set', 'game', 'total', 'points']:
                                self.game_lines[bottom_offer['label']] = self.set_game_total_points(bottom_offer['label'])
                            elif draftkings_cleaned_name == ['total', 'games', 'set']:
                                self.game_lines[bottom_offer['label']] = self.total_games_set(bottom_offer['label'])
                            elif draftkings_cleaned_name == ['correct', 'score', 'set']:
                                self.game_lines[bottom_offer['label']] = self.total_games_set(bottom_offer['label'])
                            elif draftkings_cleaned_name == ['set', 'game', 'correct', 'score']:
                                self.game_lines[bottom_offer['label']] = self.set_game_correct_score(bottom_offer['label'])
                            elif draftkings_cleaned_name == ['set', 'game', 'to', 'deuce']:
                                self.game_lines[bottom_offer['label']] = self.set_game_to_deuce(bottom_offer['label'])
                            elif draftkings_cleaned_name == ['set', 'race', 'to', 'games']:
                                self.game_lines[bottom_offer['label']] = self.set_race_to_games(bottom_offer['label'])
                            elif draftkings_cleaned_name ==  ['score', 'after', 'games', 'set']:
                                self.game_lines[bottom_offer['label']] = self.score_after_games_set(bottom_offer['label'])
                            else:
                                print("remaining -> ",self.strip_game_line(bottom_offer['label']), bottom_offer['label'])
                                pass
                        else:
                            print('line is closed', bottom_offer['label'])
    def score_after_games_set(self, draftkings_raw_name):
        cleaned_draftkings_name_array = draftkings_raw_name.replace("|", "").replace("-", "").lower().split()
        curr_set = cleaned_draftkings_name_array[4][0]
        curr_game = cleaned_draftkings_name_array[2]
        return GameLine(line_name = draftkings_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None)

    def set_race_to_games(self, draftkings_raw_name):
        cleaned_draftkings_name_array = draftkings_raw_name.replace("|", "").replace("-", "").lower().split()
        curr_set = cleaned_draftkings_name_array[1]
        curr_game = cleaned_draftkings_name_array[4]
        return GameLine(line_name = draftkings_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None)

    def set_game_to_deuce(self, draftkings_raw_name):
        cleaned_draftkings_name_array = draftkings_raw_name.replace("|", "").replace("-", "").lower().split()
        curr_set = cleaned_draftkings_name_array[1]
        curr_game = cleaned_draftkings_name_array[3]
        return GameLine(line_name = draftkings_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None)

    def set_game_correct_score(self, draftkings_raw_name):
        cleaned_draftkings_name_array = draftkings_raw_name.replace("|", "").replace("-", "").lower().split()
        curr_set = cleaned_draftkings_name_array[1]
        curr_game = cleaned_draftkings_name_array[3]
        return GameLine(line_name = draftkings_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None)

    def correct_score_set(self, draftkings_raw_name):
        cleaned_draftkings_name_array = draftkings_raw_name.replace("|", "").replace("-", "").lower().split()
        curr_set = cleaned_draftkings_name_array[2]
        return GameLine(line_name = draftkings_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None)

    def total_games_set(self, draftkings_raw_name):
        cleaned_draftkings_name_array = draftkings_raw_name.replace("|", "").replace("-", "").lower().split()
        curr_set = cleaned_draftkings_name_array[2][0]
        return GameLine(line_name = draftkings_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None)

    def set_game_total_points(self, draftkings_raw_name ): 
        cleaned_draftkings_name_array = draftkings_raw_name.replace("|", "").replace("-", "").lower().split()
        curr_set = cleaned_draftkings_name_array[1]
        curr_game = cleaned_draftkings_name_array[3]
        return GameLine(line_name = draftkings_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None)

    def set_game_point_winner(self, draftkings_raw_name):
        cleaned_draftkings_name_array = draftkings_raw_name.replace("|", "").replace("-", "").lower().split()
        curr_set = cleaned_draftkings_name_array[1]
        curr_game = cleaned_draftkings_name_array[3]
        point_in_game = cleaned_draftkings_name_array[5] #['set', '1', 'game', '4', 'point', '3', 'winner'] 
        #Not saving point_in_game because no data stored on the sofascore side quite yet
        return GameLine(line_name = draftkings_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None)
 
    def set_game_winner(self, draftkings_raw_name):
        cleaned_draftkings_name_array = draftkings_raw_name.replace("|", "").replace("-", "").lower().split()
        curr_set = cleaned_draftkings_name_array[1]
        curr_game = cleaned_draftkings_name_array[3]
        return GameLine(line_name = draftkings_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None)

    def _set_(self, draftkings_raw_name):
        cleaned_draftkings_name_array = draftkings_raw_name.replace("|", "").replace("-", "").lower().split()
        curr_set = cleaned_draftkings_name_array[0][0]
        return GameLine(line_name = draftkings_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None)
    
    def total_games(self, outcomes): #yeah not sure quite how to deal with this one
        #gather all of the information, and then check it against the total games count
        outcome_arr = []
        for outcome in outcomes:
            outcome_arr.append(outcome["line"])
        print("outcome arr", outcome_arr)



def test_full_code(type):
    ans = collections.defaultdict()
    if type == 'local':
        print("test local beginning")
        json_res = json.load(open('dk_current_event.json'))
        timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    elif type == 'online':
        res = dk_main()
        timestamp, json_res = res['timestamp'], res['ans']
        subfolder = f'draftkings/draftkings_{timestamp}' + '.json'
    count = 0

    print("Number of Games", len(json_res))

    for test_event in json_res:
        ingested_draftkings = DraftkingsGameState(json_res[test_event])
        ans[ingested_draftkings.event_name] = ingested_draftkings
        count += 1 
    return ans

    
#parse the json to get lines like a game event's moneyline
#load some of the json

def clean_event_name(json):
    def remove_first_name_from_halves_doubles(half):
        half = half.strip()
        back_slash_index = half.index("/")
        first_player_team_x = half[0:back_slash_index]
        second_player_team_x = half[back_slash_index+1:]

        last_name_first_player, last_name_second_player = first_player_team_x, second_player_team_x
        try:
            last_name_first_player = first_player_team_x[first_player_team_x.rindex(" ") + 1:]
        except:
            pass
        try:
            last_name_second_player = second_player_team_x[second_player_team_x.rindex(" ") + 1:]
        except:
            pass
        # print(last_name_first_player, last_name_second_player)
        return last_name_first_player, last_name_second_player

    def remove_first_name_from_singles(half):
        half = half.strip()
        space_index = half.rindex(" ")
        if space_index != -1:
            #print('last name -> singles ->', half[space_index+1:])
            return half[space_index+1:]

    #print("uncleaned event_name", json)
    clean_slash = json.replace(" / ", "/").replace("@", "vs")
    #print('changed @ sign', clean_slash)

    first_half, second_half = clean_slash[0:clean_slash.index("vs")], clean_slash[clean_slash.index("vs") + 2:]
    #print("halves", first_half, second_half)

    if '/' in first_half and '/' in second_half:
        player_one, player_two = remove_first_name_from_halves_doubles(first_half)
        player_three, player_four = remove_first_name_from_halves_doubles(second_half)
        #print('final res doubles', player_one + '/' + player_two + " vs " + player_three + "/" + player_four, "\n")
        print(player_one + '/' + player_two + " vs " + player_three + "/" + player_four)
        return player_one + '/' + player_two + " vs " + player_three + "/" + player_four

    else:
        ans = remove_first_name_from_singles(first_half) + ' vs ' + remove_first_name_from_singles(second_half)
        #print('final res singles', ans, "\n")
        print(ans)
        return ans


if __name__ == "__main__":
    # res = test_full_code('online')
    res = test_full_code('local')
    # print("random things")
    # for item in res:
    #     for attribute in (vars(res[item])):
    #         print(attribute, vars(res[item])[attribute])