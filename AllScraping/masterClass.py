

import copy
from sofascoreParser import *
import caesarsParser as caesarsParser
import draftkingsParser as draftkingsParser
import fanduelParser as fanduelParser
import streamlit as st





def print_sofaScore_without_json(sofascore):
    copy_state = copy.copy(sofascore)
    copy_state = copy_state.__dict__

    del copy_state['input']
    #print("\tSOFA INFO ->",copy_state)
    uprint(copy_state)


def main():
    sofascore_main()
    allSofascoreGamesDict = ingest_softscore_data()
    allCaesarsGamesDict = caesarsParser.test_full_code("online")  
    allDraftkingsGamesDict = draftkingsParser.test_full_code("online")
    allFanduelGamesDict = fanduelParser.test_full_code("online")
    #get the intersection of two arrays

    print('CAESARS GAMES ', allCaesarsGamesDict.keys())
    print('SOFA GAMES ',allSofascoreGamesDict.keys())
    print("DRAFTKINGS GAMES", allDraftkingsGamesDict.keys())
    print("FANDUEL GAMES", allFanduelGamesDict.keys())

    print()
    caesars_intersection = allSofascoreGamesDict.keys() & allCaesarsGamesDict.keys() 
    draftkings_intersection = allSofascoreGamesDict.keys() & allDraftkingsGamesDict.keys() 
    fanduel_intersection = allSofascoreGamesDict.keys() & allFanduelGamesDict.keys() 

    print("CAESARS INTERSECTIONS -> " , caesars_intersection)
    print("DRAFTKINGS INTERSECTIONS -> " , draftkings_intersection)
    print("FANDUEL INTERSECTION-> ", fanduel_intersection)

    #note that sofascore has some reads as this their data is already passed...
        #Ex: curr_set = 1. This means it is still set 1
        #curr game = 5 means they are in game 5
        #And curr points = 3 means that they are fighting for point 4 currently
        #total points and total games seems to be off so not sure there entirely
        
    #iterate through intersection 
    for item in caesars_intersection:
        """
        ANALYZING CAESARS GAMES
        """
        print("GAME EVENT NAME BEING ANALYZED ...", item)
        caesarsEvent = allCaesarsGamesDict[item]
        sofaScoreEvent = allSofascoreGamesDict[item]
        for caesars_game_line_key in caesarsEvent.game_lines:
            caesars_game_line = caesarsEvent.game_lines[caesars_game_line_key]
            print(caesars_game_line_key)
            print("\tCAESARS INFO -> ", vars(caesars_game_line))
            print_sofaScore_without_json(sofaScoreEvent)
            #compare matches against each other

            """
            WARNING: IF YOU WANT WANT TO SEARCH FOR POINTS, THEN SET AND GAME MUST MATCH
            IF YOU WANT TO SEARCH FOR GAME, THEN SET MUST MATCH
            THE BELOW CODE FOR CHECKING ON GAMES IS ENTIRELY WRONG. MUST BE A CASCADE
            """

            #check for lagging set
            #check if the set is the same, then check for a lagging game
            #check if the set and the game is the same, then check for a lagging point


            #set_game_point check 

            #just a set check
            #just a game check
            #just a point check

            #set and game 
            #set and point

            #game and point

            #hey your events are still messed up

            if caesars_game_line.curr_set and caesars_game_line.curr_game and caesars_game_line.curr_point:
                print("then do set game point comparison")
            elif caesars_game_line.curr_set and caesars_game_line.curr_game and caesars_game_line.curr_point == None:
                print("testing")
            elif caesars_game_line.curr_set and caesars_game_line.curr_game == None and caesars_game_line.curr_point == None:
                print("testing")


            if caesars_game_line.curr_set and sofaScoreEvent.curr_set:
                if (caesars_game_line.curr_set < sofaScoreEvent.curr_set): 
                    print('\t\tcurr_set GLITCH', f"caesars curr_set: {caesars_game_line.curr_set} sofa curr_set: {sofaScoreEvent.curr_set}")
                elif (caesars_game_line.curr_set == sofaScoreEvent.curr_set): 
                    if caesars_game_line.curr_game and sofaScoreEvent.curr_game:
                        if (caesars_game_line.curr_game < sofaScoreEvent.curr_game): 
                            print('\t\tcurr_game GLITCH  |  ', f"caesars curr_game: {caesars_game_line.curr_game} sofa curr_game: {sofaScoreEvent.curr_game}")
                    elif caesars_game_line.points and sofaScoreEvent.points:
                        if (caesars_game_line.points <= sofaScoreEvent.points): 
                            print('\t\tpoints GLITCH  |  ', f"caesars points: {caesars_game_line.points} sofa points: {sofaScoreEvent.points}")
            



            print()
        #so curr_set should be the same

    for item in draftkings_intersection:
        """
        ANALYZING DRAFTKINGS GAMES
        """
        print("Game event name being analyzed...", item)
        draftkingsEvent = allDraftkingsGamesDict[item]
        sofaScoreEvent = allSofascoreGamesDict[item]
        
        for draftkings_game_line_key in draftkingsEvent.game_lines:
            draftkings_game_line = draftkingsEvent.game_lines[draftkings_game_line_key]
            try:
                print(draftkings_game_line.__dict__)
            except Exception as e:
                print(e)
                print("item", draftkings_game_line)

if __name__ == "__main__":
    # main()
    print('some shit')