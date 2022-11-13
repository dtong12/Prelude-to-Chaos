

import copy
from sofascoreParser import *
import caesarsParser as caesarsParser
import draftkingsParser as draftkingsParser
import fanduelParser as fanduelParser
import streamlit as st
import sofascoreCurrentEvents as sofascoreCurrentEvents




def print_sofaScore_without_json(sofascore):
    copy_state = copy.copy(sofascore)
    copy_state = copy_state.__dict__

    del copy_state['input']
    #print("\tSOFA INFO ->",copy_state)
    sofascoreCurrentEvents.uprint(copy_state)

def print_sofaScoreEvent_without_input(sofascoreEvent):
    copy_state = copy.copy(sofascoreEvent)
    del copy_state.input
    print("copy state post delete", vars(copy_state))
    return vars(copy_state)


def main():
    
    """
    gameLine set is telling you what set its currently on
    sofaScore event tells you what set its currently on

    gameLine game is telling what you what games it on
    sofaScore event as well

    sofaScore points is lagging behind.... so if it says point 8, it's currently point 9
    gameLine points is telling you the available bet
    so just make sure to increment sofascore points by 1

    Ex: sofascore points is 3, meaning players are playing for point 4.
    If gameline is for game 2, point 3 that's a glitch.
    Without this note, you may have compared sofascore point 3 <= gameline points which wouldn't raise an alarm
    """
    def game_state_glitch_check(sportsbook, sofaScoreEvent, gameLine):

        print(f"\n {sportsbook}GLITCH CHECK")
        print("sofascore dict", print_sofaScoreEvent_without_input(sofaScoreEvent))
        print("gameLine dict", gameLine.__dict__)

        glitch = 0
        if gameLine.curr_set and sofaScoreEvent.curr_set: 
            if gameLine.curr_set < sofaScoreEvent.curr_set: #then that set on the sportsbook is passed
                print("glitch in set")
        if gameLine.curr_set and sofaScoreEvent.curr_set and gameLine.curr_game and sofaScoreEvent.curr_game:
            if gameLine.curr_set == sofaScoreEvent.curr_set:
                if gameLine.curr_game < sofaScoreEvent.curr_game:
                    print("glitch game")
        if gameLine.curr_set and sofaScoreEvent.curr_set and gameLine.curr_game and sofaScoreEvent.curr_game and gameLine.curr_points and sofaScoreEvent.curr_points:
             if gameLine.curr_set == sofaScoreEvent.curr_set:
                if gameLine.curr_game == sofaScoreEvent.curr_game:
                    #gameline point 4, sofascore point 4, whcih means point 5
                    if gameLine.curr_points < sofaScoreEvent.curr_points: #sofascore is ahead by one 
                        print("glitch in point")






    st.title("Current Games")
    col1, col2, col3, col4 = st.columns(4)

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


    st.header("Anchored Games")
    st.write("Caesars matches: ", list(caesars_intersection))
    st.write("Draftkings matches: ", list(draftkings_intersection))
    st.write("Fanduel matches: ", list(fanduel_intersection))

    with col1:
        st.header("Sofascore")
        for item in sorted(allSofascoreGamesDict.keys()):
            st.markdown(f"\t - {item}")
    with col2:
        st.header("Caesars")
        for item in sorted(allCaesarsGamesDict.keys()):
            st.markdown(f"\t - {item}")
    with col3:
        st.header("Draftkings")
        for item in sorted(allDraftkingsGamesDict.keys()):
            st.markdown(f"\t - {item}")
    with col4:
        st.header("Fanduel")
        for item in sorted(allFanduelGamesDict.keys()):
            st.markdown(f"\t - {item}")

    #note that sofascore has some reads as this their data is already passed...
        #Ex: curr_set = 1. This means it is still set 1
        #curr game = 5 means they are in game 5
        #And curr points = 3 means that they are fighting for point 4 currently
        #total points and total games seems to be off so not sure there entirely
    st.header("Lagging lines")
    
    st.header('Game Lines')
    def display_gameline_expander(sportsbook, sportsbookDict):
        with st.expander(f"{sportsbook} Games"):
            for key in sportsbookDict:
                st.markdown(f"Event name: {key}")
                for gameline in sportsbookDict[key].game_lines:
                    st.markdown(f"\t{gameline}")

    display_gameline_expander("Draftkings", allDraftkingsGamesDict)
    display_gameline_expander("Fanduel", allFanduelGamesDict)
    display_gameline_expander("Caesars", allCaesarsGamesDict)

    #iterate through intersection 
    for item in caesars_intersection:
        """
        ANALYZING CAESARS GAMES
        """
        print("Caesars Game Being Analyzed ...", item)
        caesarsEvent = allCaesarsGamesDict[item]
        sofaScoreEvent = allSofascoreGamesDict[item]
        for caesars_game_line_key in caesarsEvent.game_lines:
            caesars_game_line = caesarsEvent.game_lines[caesars_game_line_key]
            game_state_glitch_check('caesars', sofaScoreEvent, caesars_game_line)

        #so curr_set should be the same


    for item in draftkings_intersection:
        """
        ANALYZING DRAFTKINGS GAMES
        """
        print("Draftkings Game Being Analyzed...", item)
        draftkingsEvent = allDraftkingsGamesDict[item]
        sofaScoreEvent = allSofascoreGamesDict[item]
        
        for draftkings_game_line_key in draftkingsEvent.game_lines:
            draftkings_game_line = draftkingsEvent.game_lines[draftkings_game_line_key]
            game_state_glitch_check('draftkings', sofaScoreEvent, draftkings_game_line)

    for item in fanduel_intersection:
        """
        ANALYZING FANDUEL GAMES
        """
        print("fanduel Game Being Analyzed...", item)
        fanduelEvent = allFanduelGamesDict[item]
        sofaScoreEvent = allSofascoreGamesDict[item]
        
        for fanduel_game_line_key in fanduelEvent.game_lines:
            fanduel_game_line = fanduelEvent.game_lines[fanduel_game_line_key]
            game_state_glitch_check('fanduel', sofaScoreEvent, fanduel_game_line)

    
if __name__ == "__main__":
    main()
    # print('some shit')