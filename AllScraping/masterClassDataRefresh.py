

import copy
import sofascoreParser as sofascoreParser
import caesarsParser as caesarsParser
import draftkingsParser as draftkingsParser
import fanduelParser as fanduelParser
import sofascoreCurrentEvents as sofascoreCurrentEvents
import utils as utils
import mgmParser as mgmParser

import draftkingsCurrentEvents_vegas as draftkingsCurrentEvents_vegas
import fanduelCurrentEvents as fanduelCurrentEvents
import caesarsCurrentEvents as caesarsCurrentEvents

import testing_full_async_payload as async_payload

import pytz
from datetime import timedelta
import time
import os
import asyncio
from functools import wraps, partial
import beepy as beep
import json

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
    print("wiping streamlit payload -> ", "streamlit payload->", streamlit_json_payload)
    global_glitches = []
    timestamp = datetime.now(pytz.timezone('US/Eastern')).strftime("%Y_%m_%d %H:%M:%S")

    def game_state_glitch_check(sportsbook, sofaScoreEvent, gameLine, item):
        print(f"\n {sportsbook} GLITCH CHECK")
        sofascoreParser.uprint(return_sofaScoreEvent_without_input(sofaScoreEvent))
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
                        #gameline point 4, sofascore point 4, whcih means the actual game is at point 5 (confirmed seperately nov 25)
                        print("gameline points", type(gameLine.curr_points), gameLine.curr_points)
                        print("sofascoreEvent points", type(sofaScoreEvent.curr_points), sofaScoreEvent.curr_points)
                        if gameLine.curr_points < sofaScoreEvent.curr_points: #the actual game is ahead by one 
                            print("glitch in point")
                            glitches += "glitch in point"
                        #elif gameLine.curr_points >= sofaScoreEvent.curr_points:
                        point_matching = f"-   Point -> Sofa: {sofaScoreEvent.curr_points } {sportsbook}: {gameLine.curr_points}" 

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
    
    """
    Official start to the page
    """
    start_time = time.time()

    allSofascoreGamesDict, allCaesarsGamesDict, allDraftkingsGamesDict, allFanduelGamesDict, allMgmGamesDict, allBetriversGamesDict, allBarstoolsGamesDict, allTwinspiresGamesDict, allUnibetGamesDict = async_payload.thread_pool_executor()

    print(" \n ------- Raw Keys ------- ")
    print("transplant res sofa", allSofascoreGamesDict.keys())
    print("transplant res draft", allDraftkingsGamesDict.keys())
    print("transplant res caesars", allCaesarsGamesDict.keys())
    print("transplant res fanduel", allFanduelGamesDict.keys())
    print("transplant res mgm", allMgmGamesDict.keys())
    print("transplant res betrivers", allBetriversGamesDict.keys())
    print("transplant res barstools", allBarstoolsGamesDict.keys())
    print("transplant res twinspires", allTwinspiresGamesDict.keys())
    print("transplant res unibet", allUnibetGamesDict.keys())

    # print()
    caesars_intersection = allSofascoreGamesDict.keys() & allCaesarsGamesDict.keys() 
    draftkings_intersection = allSofascoreGamesDict.keys() & allDraftkingsGamesDict.keys() 
    fanduel_intersection = allSofascoreGamesDict.keys() & allFanduelGamesDict.keys() 
    mgm_intersection = allSofascoreGamesDict.keys() & allMgmGamesDict.keys()
    betrivers_intersection = allSofascoreGamesDict.keys() & allBetriversGamesDict.keys()
    barstools_intersection = allSofascoreGamesDict.keys() & allBarstoolsGamesDict.keys()
    twinspires_intersection = allSofascoreGamesDict.keys() & allTwinspiresGamesDict.keys()
    unibet_intersection = allSofascoreGamesDict.keys() & allUnibetGamesDict.keys()

    print("\n ------- Game Intersections -------")
    print("Caesars intersection", caesars_intersection)
    print("Draftkings intersection", draftkings_intersection)
    print("Fanduel intersection", fanduel_intersection)
    print("mgm intersection", mgm_intersection)
    print("betrivers intersection", betrivers_intersection)
    print("barstools intersection", barstools_intersection)
    print("twinspires intersection", twinspires_intersection)
    print("unibet intersection", unibet_intersection)

    streamlit_json_payload['analysis'] = {
        "caesars": {},
        "draftkings": {},
        "fanduel": {},
        "mgm": {},
        "betrivers": {},
        "barstools": {},
        "twinspires": {},
        "unibet": {}
    }

    def perform_analysis_on_line(sportsbook, intersection, sportsbookGamesDict):
        for item in intersection:
            sportsbook_event = sportsbookGamesDict[item]
            sofaScoreEvent = allSofascoreGamesDict[item]
            print("performing analysis on line", sportsbook, 'game -> ',item)
            for game_line_key in sportsbook_event.game_lines:
                game_line = sportsbook_event.game_lines[game_line_key]
                game_state_glitch_check(sportsbook, sofaScoreEvent, game_line, item)

    #Calculating Lines with Analysis

    perform_analysis_on_line('caesars', caesars_intersection, allCaesarsGamesDict)
    perform_analysis_on_line('draftkings', draftkings_intersection, allDraftkingsGamesDict)
    perform_analysis_on_line('fanduel', fanduel_intersection, allFanduelGamesDict)
    perform_analysis_on_line('mgm', mgm_intersection, allMgmGamesDict)
    perform_analysis_on_line('betrivers', betrivers_intersection, allBetriversGamesDict)
    perform_analysis_on_line('barstools', barstools_intersection, allBarstoolsGamesDict)
    perform_analysis_on_line('twinspires', barstools_intersection, allTwinspiresGamesDict)
    perform_analysis_on_line('twinspires', barstools_intersection, allUnibetGamesDict)

    print("\n============================================")
    print("\nglobal glitches length", len(global_glitches), global_glitches)
    if len(global_glitches) != 0:
        beep.beep(1)
        print("Data saved")
        file = open("glitch_counter.txt", "w")
        file.write(f"{timestamp} -> {global_glitches}\n")
        # utils.send_email(global_glitches)
    
    # NO GAME LINE ANALYSIS
    streamlit_json_payload['no_analysis'] = {}
    def display_gameline_expander(sportsbook, sportsbookDict):
        if sportsbook not in streamlit_json_payload['no_analysis']:
            streamlit_json_payload['no_analysis'][sportsbook] = {}
        for key in sportsbookDict:
            if key not in streamlit_json_payload['no_analysis']:
                streamlit_json_payload['no_analysis'][sportsbook][key] = {}
            for gameline in sportsbookDict[key].game_lines:
                if gameline not in streamlit_json_payload['no_analysis'][sportsbook][key]:
                    streamlit_json_payload['no_analysis'][sportsbook][key][gameline] = []
                streamlit_json_payload['no_analysis'][sportsbook][key][gameline].append(gameline)

    display_gameline_expander("caesars", allCaesarsGamesDict)
    display_gameline_expander("draftkings", allDraftkingsGamesDict)
    display_gameline_expander("fanduel", allFanduelGamesDict)
    display_gameline_expander("mgm", allMgmGamesDict)
    display_gameline_expander("betrivers", allBetriversGamesDict)
    display_gameline_expander("barstools", allBarstoolsGamesDict)
    display_gameline_expander("twinspires", allTwinspiresGamesDict)
    display_gameline_expander("unibet", allUnibetGamesDict)

    """
    Standardizing all game data underneath this
    """
    streamlit_json_payload['timestamp'] = timestamp
    streamlit_json_payload['game_names'] = {}
    streamlit_json_payload['game_names']['sofa_games'] = list(allSofascoreGamesDict.keys())
    streamlit_json_payload['game_names']['caesars_games'] = list(allCaesarsGamesDict.keys())
    streamlit_json_payload['game_names']['draftkings_games'] = list(allDraftkingsGamesDict.keys())
    streamlit_json_payload['game_names']['fanduel_games'] = list(allFanduelGamesDict.keys())
    streamlit_json_payload['game_names']['mgm_games'] = list(allMgmGamesDict.keys())
    streamlit_json_payload['game_names']['betrivers_games'] = list(allBetriversGamesDict.keys())
    streamlit_json_payload['game_names']['barstools_games'] = list(allBarstoolsGamesDict.keys())
    streamlit_json_payload['game_names']['twinspires_games'] = list(allTwinspiresGamesDict.keys())
    streamlit_json_payload['game_names']['unibet_games'] = list(allUnibetGamesDict.keys())
    

    streamlit_json_payload['intersection'] = {}
    streamlit_json_payload['intersection']['caesars_games'] = list(caesars_intersection)
    streamlit_json_payload['intersection']['draftkings_games'] = list(draftkings_intersection)
    streamlit_json_payload['intersection']['fanduel_games'] = list(fanduel_intersection)
    streamlit_json_payload['intersection']['mgm_games'] = list(mgm_intersection)
    streamlit_json_payload['intersection']['betrivers_games'] = list(betrivers_intersection)
    streamlit_json_payload['intersection']['barstools_games'] = list(barstools_intersection)
    streamlit_json_payload['intersection']['twinspires_games'] = list(twinspires_intersection)
    streamlit_json_payload['intersection']['unibet_games'] = list(unibet_intersection)
    streamlit_json_payload['global_glitches'] = global_glitches

    with open('latest_streamlit_json_payload.json', 'w') as f:
        json.dump(streamlit_json_payload, f)
    print("data saved.")

    print("Total time: --- %s seconds ---" % (time.time() - start_time))
    print("start time: ", timestamp)
    # f.close()

    return streamlit_json_payload
if __name__ == "__main__":
    main()