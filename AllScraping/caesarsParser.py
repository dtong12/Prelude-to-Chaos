from caesarsCurrentEvents import *
import re




"""
Methodology:
1: Strip all of the weird symbols
2. If each of the word profiles match exactly (remove all of the numbers and see if the arrays are the same)
    2a. word profile for "Set Winner Live" -> [|Set|, |Winner|, |Live|]
    2b: |2nd| |Set| |Winner| |Live|  gets reduced to [|Set| |Winner| |Live|]
Identified lines:
|2nd| |Set| |Winner| |Live| 
|2nd| |Set| - |Game| 6 |Live|

"""

#Weirder lines -> # 
# 3rd Set - Games 2 And 3 - To Win Both Games

# profiles = {
#     'Set Winner Live': ['|set|', '|winner|', '|live| '],
#     'Set Game Live': ['|set|', '|game|', '|live|']
# }

profiles = [
    ['set', 'winner', 'live'], #"1st Set Winner Live"
    ['set', 'game', 'live'], #1st Set - Game 10 Live
    ['set', 'game'], # 3rd Set - Game 6

    #not completed yet
    ['set', 'betting', 'live'],  #Set betting live #DNE requires sub line reading
    ['set', 'total', 'games', 'odd/even'], #3rd Set - Total Games Odd/Even, DNE: Requires set specific data ->
    ['set', 'total', 'games', 'live'], #3rd Set - Total Games Live, DNE: Requires set specific data
    ['set', 'game', 'score', 'after', 'points'] #3rd Set - Game 3 - Score After 2 Points ->DNE requires sub line reading
]


#lines we don't have
#Set betting live
#2nd Set - Game 11
#2nd Set - Game 11 - Score After 2 Points #DNE
#2nd Set - Total Games Odd/Even
#2nd Set - Total Games Live
#2nd Set - Game 11 - Score After 2 Points
#Match Betting Live


class CaesarsGameState:
    def __init__(self, event_json):
        try:
            self.event_name = clean_event_name(event_json['json']['name'])
            self.event_json = event_json
            self.game_lines = {}
            self.get_game_lines()
        except Exception as e:
            print('caesars : error getting event name')
            exit
    
    def strip_game_line(self,game_line):
        game_line = game_line.replace("-", "").replace("|", "")
        return([i for i in re.sub(r'[.,!?]', '', game_line.lower()).split() if not re.search(r'\d', i)])

    def get_game_lines(self):
        print('event name ->',self.event_name)
        print("number of lines to read -> ", len(self.event_json['json']['markets']))
        for market in self.event_json['json']['markets']:
            caesars_stripped_line_name = self.strip_game_line(market['name'])
            # print("ALL LINES", market['name'], market['display'], market['active'])
            # if caesars_stripped_line_name in profiles and market['display'] and market['active']:
            if market['display'] and market['active']:
                print("Viable game line MATCH", caesars_stripped_line_name, "-> ", market['name'])
                if caesars_stripped_line_name == ['set', 'winner', 'live']: 
                   self.game_lines[market['name']] = (self.set_winner_live(market['name']))
                elif caesars_stripped_line_name ==  ['set', 'game', 'live']:
                    self.game_lines[market['name']] = (self.set_game_live(market['name']))
                elif caesars_stripped_line_name == ['set', 'game']:
                    self.game_lines[market['name']] = (self.set_game(market['name']))
                elif caesars_stripped_line_name == ['set', 'game', 'correct', 'score']:
                    self.game_lines[market['name']] = (self.set_game_correct_score(market['name']))
                else:
                    print("remaining -> ", caesars_stripped_line_name, market['name'])
            else:
                pass
                #print("caesars inactive lines -> ", caesars_stripped_line_name, market['name'])
        print('\n')
    def set_winner_live(self, caesars_raw_name):
        cleaned_caesars_name_array = caesars_raw_name.replace("|", "").replace("-", "").split()
        #set_num =  [int(i) for i in cleaned_caesars_name_array[0].split() if i.isdigit()]
        #print("   ",cleaned_caesars_name_array, set_num)
        curr_set = int(cleaned_caesars_name_array[0][0])
        return GameLine(line_name = caesars_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = None, curr_points = None, total_points_in_match= None, total_games_in_match= None)

    def set_game_live(self, caesars_raw_name):
        cleaned_caesars_name_array = caesars_raw_name.replace("|", "").replace("-", "").split()
        #print("cleaned array ", cleaned_caesars_name_array)
        curr_set = int(cleaned_caesars_name_array[0][0])
        curr_game = int(cleaned_caesars_name_array[3])
        return GameLine(line_name = caesars_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None)

    def set_game(self, caesars_raw_name):
        cleaned_caesars_name_array = caesars_raw_name.replace("|", "").replace("-", "").split()
        curr_set = int(cleaned_caesars_name_array[0][0])
        curr_game = int(cleaned_caesars_name_array[-1])
        #print("raw name:", caesars_raw_name, "extracted curr_game", curr_game)
        return GameLine(line_name = caesars_raw_name, cleaned_line_name= None, curr_set= curr_set, curr_game = curr_game, curr_points = None, total_points_in_match= None, total_games_in_match= None)
    
    def set_game_correct_score(self, caesars_raw_name):
        
        print("SET GAME CORRECT SCORE TRIGGERED")
        cleaned_caesars_name_array = caesars_raw_name.replace("|", "").replace("-", "").split()
        curr_set = int(cleaned_caesars_name_array[0][0])
        # print(("SET GAME CORRECT SCORE", curr_set))
        pass

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


def test_full_code(type):
    ans = collections.defaultdict()
    if type == 'local':
        print("test local beginning")
        json_res = json.load(open('ca_current_event.json'))
        timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")
    elif type == 'online':
        res = async_caesars_main() #res = caesars_main()
        timestamp, json_res = res['timestamp'], res['ans']
        subfolder = f'caesars/caesars_{timestamp}' + '.json'
    count = 0
    print("Number of Games", len(json_res))

    #PRINTS THE EVENT DETECTED AND ADDS THEM TO ANS
    for test_event in json_res:
        try:
            ingested_caesars = CaesarsGameState(json_res[test_event])
            ans[ingested_caesars.event_name] = ingested_caesars
            count += 1 
        except Exception as e:
            pass
        #url  = json_res[test_event]['url']
        #event_name = clean_event_name(json_res[test_event]['json']['name'])
        #print("event_name ->", event_name)
    return ans

def clean_event_name(json):
    def remove_first_name_from_halves_doubles(half):
        half = half.strip()
        back_slash_index = half.index("/")
        first_player_team_x = half[0:back_slash_index]
        second_player_team_x = half[back_slash_index:]

        last_name_first_player = first_player_team_x[first_player_team_x.rindex(" ") + 1:]
        last_name_second_player = second_player_team_x[second_player_team_x.rindex(" ") + 1:]

        # print('last names -> doubles ->',last_name_first_player, last_name_second_player)
        return last_name_first_player, last_name_second_player

    def remove_first_name_from_singles(half):
        half = half.strip()
        space_index = half.rindex(" ")
        if space_index != -1:
            #print('last name -> singles ->', half[space_index+1:])
            return half[space_index+1:]

    # print("json-> ", json)
    clean_slash = json.replace("|", "")
    print('clean_slash', clean_slash)
    first_half, second_half = clean_slash[0:clean_slash.index("vs")], clean_slash[clean_slash.index("vs") + 2:]
    # print("caesars halves", first_half, second_half)
    if '/' in first_half and '/' in second_half:
        player_one, player_two = remove_first_name_from_halves_doubles(first_half)
        player_three, player_four = remove_first_name_from_halves_doubles(second_half)
        # print("returned answer ->", player_one + '/' + player_two + " vs " +player_three + "/" + player_four)
        return player_one + '/' + player_two + " vs " + player_three + "/" + player_four
    else:
        return remove_first_name_from_singles(first_half) + ' vs ' + remove_first_name_from_singles(second_half)

def parse_event_name(json):
    return clean_event_name(json['name'])


if __name__ == "__main__":
    res = test_full_code("online")  
    # res = test_full_code("local")