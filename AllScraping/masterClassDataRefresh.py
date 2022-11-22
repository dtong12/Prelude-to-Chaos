

import copy
from sofascoreParser import *
import caesarsParser as caesarsParser
import draftkingsParser as draftkingsParser
import fanduelParser as fanduelParser
import streamlit as st
import sofascoreCurrentEvents as sofascoreCurrentEvents
from streamlit_autorefresh import st_autorefresh
import utils as utils

import draftkingsCurrentEvents_vegas as draftkingsCurrentEvents_vegas
import fanduelCurrentEvents as fanduelCurrentEvents
import caesarsCurrentEvents as caesarsCurrentEvents

import pytz
from datetime import timedelta
import time
import os
import asyncio
from functools import wraps, partial

from datetime import datetime
import pytz



def print_sofaScore_without_json(sofascore):
    copy_state = copy.copy(sofascore)
    copy_state = copy_state.__dict__

    del copy_state['input']
    sofascoreCurrentEvents.uprint(copy_state)

def return_sofaScoreEvent_without_input(sofascoreEvent):
    copy_state = copy.copy(sofascoreEvent)
    del copy_state.input
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
    streamlit_json_payload = {}
    global_glitches = []
    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")

    def game_state_glitch_check(sportsbook, sofaScoreEvent, gameLine, item):
        print(f"\n {sportsbook} GLITCH CHECK")
        # print("sofascore dict", return_sofaScoreEvent_without_input(sofaScoreEvent))
        uprint(return_sofaScoreEvent_without_input(sofaScoreEvent))
        print("gameLine dict", gameLine.__dict__)
        try:
            glitches = ''
            set_matching = None
            game_matching = None
            point_matching = None

            if item not in streamlit_json_payload['analysis'][sportsbook]:
                streamlit_json_payload['analysis'][sportsbook][item] = {}

            if gameLine.line_name not in streamlit_json_payload['analysis'][sportsbook][item]:
                streamlit_json_payload['analysis'][sportsbook][item][gameLine.line_name] = {
                    'set_matching': '',
                    'game_matching': '',
                    'point_matching': '',
                    'glitches': ''
                }

            if gameLine.curr_set and sofaScoreEvent.curr_set: 
                if gameLine.curr_set < sofaScoreEvent.curr_set: #then that set on the sportsbook is passed
                    print("glitch in set")
                    glitches += "glitch in set"
                #elif gameLine.curr_set >= sofaScoreEvent.curr_set:
                set_matching = f"-   Set -> Sofa: {sofaScoreEvent.curr_set } {sportsbook}: {gameLine.curr_set}" 
                    
            if gameLine.curr_set and sofaScoreEvent.curr_set and gameLine.curr_game and sofaScoreEvent.curr_game:
                if gameLine.curr_set == sofaScoreEvent.curr_set:
                    if gameLine.curr_game < sofaScoreEvent.curr_game:
                        print("glitch game")
                        glitches += "glitch in game"
                    game_matching = f"-   Game -> Sofa: {sofaScoreEvent.curr_game } {sportsbook}: {gameLine.curr_game}" 
            if gameLine.curr_set and sofaScoreEvent.curr_set and gameLine.curr_game and sofaScoreEvent.curr_game and gameLine.curr_points and sofaScoreEvent.curr_points:
                if gameLine.curr_set == sofaScoreEvent.curr_set:
                    if gameLine.curr_game == sofaScoreEvent.curr_game:
                        #gameline point 4, sofascore point 4, whcih means the actual game is at point 5
                        print("gameline points", type(gameLine.curr_points), gameLine.curr_points)
                        print("sofascoreEvent points", type(sofaScoreEvent.curr_points), sofaScoreEvent.curr_points)
                        if gameLine.curr_points < sofaScoreEvent.curr_points: #the actual game is ahead by one 
                            print("glitch in point")
                            glitches += "glitch in point"
                        #elif gameLine.curr_points >= sofaScoreEvent.curr_points:
                        point_matching = f"-   Point -> Sofa: {sofaScoreEvent.curr_points } {sportsbook}: {gameLine.curr_points}" 

            st.markdown(f'<h1 style="color:#FFFFFF;font-size:18px;">{gameLine.line_name}</h1>', unsafe_allow_html=True)
            print('game_matching', game_matching)

            if set_matching: streamlit_json_payload['analysis'][sportsbook][item][gameLine.line_name]['set_matching'] = set_matching
            if game_matching: streamlit_json_payload['analysis'][sportsbook][item][gameLine.line_name]['game_matching'] = game_matching
            if point_matching: streamlit_json_payload['analysis'][sportsbook][item][gameLine.line_name]['point_matching'] = point_matching
            if glitches: streamlit_json_payload['analysis'][sportsbook][item][gameLine.line_name]['glitches'] = glitches
            #doing line analysis at the end MOOSE

            #Add glitches to global_glitches at the end
            if glitches != '':
                print("Glitch detected... aggregating all glitches")
                payload = {
                    "sportsbook":sportsbook, 
                    "game name": item, 
                    "line_name": gameLine.line_name, 
                    "glitch type": glitches
                }
                config = {"set_matching": set_matching, "game_matching": game_matching, "point_matching": point_matching}
                for key in config:
                    if config[key]:
                        payload[key] = config[key]
                global_glitches.append(payload)
        except Exception as e:
            print('Exception: ', repr(e))
            st.markdown(f'<h1 style="color:#FAC898;font-size:10px;">Exceptions: {e} {gameLine.line_name}</h1>', unsafe_allow_html=True)
    
    """
    Official start to the page
    """
    start_time = time.time()
    st.title("Prelude To Chaos")
    col1, col2, col3, col4 = st.columns(4)

    async_sofascore_main() # sofascore_main()
    allSofascoreGamesDict = ingest_softscore_data()
    allCaesarsGamesDict = caesarsParser.test_full_code("online")  
    allDraftkingsGamesDict = draftkingsParser.test_full_code("online")
    allFanduelGamesDict = fanduelParser.test_full_code("online")
    #get the intersection of two arrays 

    # print()
    caesars_intersection = allSofascoreGamesDict.keys() & allCaesarsGamesDict.keys() 
    draftkings_intersection = allSofascoreGamesDict.keys() & allDraftkingsGamesDict.keys() 
    fanduel_intersection = allSofascoreGamesDict.keys() & allFanduelGamesDict.keys() 
    
    
    streamlit_json_payload['analysis'] = {
        "caesars": {},
        "draftkings": {},
        "fanduel": {}
    }

    def perform_analysis_on_line(sportsbook, intersection, sportsbookGamesDict):
        print("printing analysis on line", sportsbook)
        st.header(sportsbook.capitalize())
        with st.expander(f"{sportsbook.capitalize()} Games"):
            for item in intersection:
                sportsbook_event = sportsbookGamesDict[item]
                sofaScoreEvent = allSofascoreGamesDict[item]
                st.markdown(f'<h1 style="color:#FAF9F6;font-size:20px;"> Event Name: {item}</h1>', unsafe_allow_html=True)
                for game_line_key in sportsbook_event.game_lines:
                    game_line = sportsbook_event.game_lines[game_line_key]
                    game_state_glitch_check(sportsbook, sofaScoreEvent, game_line, item)

    #Calculating Lines with Analysis
    st.header("Lines Covered - with Analysis")
    col1, col2, col3 = st.columns(3)
    with col1: 
        perform_analysis_on_line('caesars', caesars_intersection, allCaesarsGamesDict)
    with col2: 
        perform_analysis_on_line('draftkings', draftkings_intersection, allDraftkingsGamesDict)
    with col3: 
        perform_analysis_on_line('fanduel', fanduel_intersection, allFanduelGamesDict)

    st.write("Global glitches", global_glitches)
    print("\n============================================")
    print("\nglobal glitches length", len(global_glitches), global_glitches)
    if len(global_glitches) != 0:
        print("Data saved")
        utils.send_email(global_glitches)
    

    # NO GAME LINE ANALYSIS
    st.header('Covered Lines - No analysis')
    streamlit_json_payload['no_analysis'] = {}
    col1, col2, col3 = st.columns(3)
    def display_gameline_expander(sportsbook, sportsbookDict):
        if sportsbook not in streamlit_json_payload['no_analysis']:
            streamlit_json_payload['no_analysis'][sportsbook] = {}
        with st.expander(f"{sportsbook} Games"):
            for key in sportsbookDict:
                if key not in streamlit_json_payload['no_analysis']:
                    streamlit_json_payload['no_analysis'][sportsbook][key] = {}
                for gameline in sportsbookDict[key].game_lines:
                    st.markdown(f"\t{gameline}")
                    if gameline not in streamlit_json_payload['no_analysis'][sportsbook][key]:
                        streamlit_json_payload['no_analysis'][sportsbook][key][gameline] = []
                    streamlit_json_payload['no_analysis'][sportsbook][key][gameline].append(gameline)

    with col1: display_gameline_expander("caesars", allCaesarsGamesDict)
    with col2: display_gameline_expander("draftkings", allDraftkingsGamesDict)
    with col3: display_gameline_expander("fanduel", allFanduelGamesDict)


    """
    Standardizing all game data underneath this
    """
    streamlit_json_payload['timestamp'] = timestamp
    streamlit_json_payload['game_names'] = {}
    streamlit_json_payload['game_names']['sofa_games'] = list(allSofascoreGamesDict.keys())
    streamlit_json_payload['game_names']['caesars_games'] = list(allCaesarsGamesDict.keys())
    streamlit_json_payload['game_names']['draftkings_games'] = list(allDraftkingsGamesDict.keys())
    streamlit_json_payload['game_names']['fanduel_games'] = list(allFanduelGamesDict.keys())
    streamlit_json_payload['intersection'] = {}
    streamlit_json_payload['intersection']['caesars_games'] = list(caesars_intersection)
    streamlit_json_payload['intersection']['draftkings_games'] = list(draftkings_intersection)
    streamlit_json_payload['intersection']['fanduel_games'] = list(fanduel_intersection)

    streamlit_json_payload['global_glitches'] = global_glitches

    with open('AllScraping/latest_streamlit_json_payload.json', 'w') as f:
        #AllScraping\latest_streamlit_json_payload.json
        json.dump(streamlit_json_payload, f)

    print("Total time: --- %s seconds ---" % (time.time() - start_time))
    print("start time: ", timestamp)
    f.close()
if __name__ == "__main__":
    main()    
    # while True:
    #     try:
    #         main()
    #     except:
    #         pass
    #     time.sleep(25)