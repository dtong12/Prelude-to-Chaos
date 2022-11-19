

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
st_autorefresh(interval=1 * 60 * 1000, key="dataframerefresh") #once a minute


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

    global_glitches = []

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
                    #elif gameLine.curr_game >= sofaScoreEvent.curr_game:
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
            if set_matching:
                st.markdown(f'<h1 style="color:#33ff33;font-size:14px;">{set_matching}</h1>', unsafe_allow_html=True)
            if game_matching:
                st.markdown(f'<h1 style="color:#33ff33;font-size:14px;">{game_matching}</h1>', unsafe_allow_html=True)
            if point_matching:
                st.markdown(f'<h1 style="color:#33ff33;font-size:14px;">{point_matching}</h1>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="color:#ff6961;font-size:10px;">Glitches: {glitches}</h1>', unsafe_allow_html=True)
            
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
            print('Exception: ', e)
            st.markdown(f'<h1 style="color:#FAC898;font-size:10px;">Exceptions: {e} {gameLine.line_name}</h1>', unsafe_allow_html=True)
        

    """
    Official start to the page
    """

    st.title("Prelude To Chaos")
    col1, col2, col3, col4 = st.columns(4)

    async_sofascore_main() # sofascore_main()
    allSofascoreGamesDict = ingest_softscore_data()
    allCaesarsGamesDict = caesarsParser.test_full_code("online")  
    allDraftkingsGamesDict = draftkingsParser.test_full_code("online")
    allFanduelGamesDict = fanduelParser.test_full_code("online")
    #get the intersection of two arrays

    print('CAESARS GAMES ', allCaesarsGamesDict.keys())
    print('SOFA GAMES ',allSofascoreGamesDict.keys())
    print("DRAFTKINGS GAMES", allDraftkingsGamesDict.keys())
    print("FANDUEL GAMES", allFanduelGamesDict.keys())

    # print()
    caesars_intersection = allSofascoreGamesDict.keys() & allCaesarsGamesDict.keys() 
    draftkings_intersection = allSofascoreGamesDict.keys() & allDraftkingsGamesDict.keys() 
    fanduel_intersection = allSofascoreGamesDict.keys() & allFanduelGamesDict.keys() 

    print("CAESARS INTERSECTIONS -> " , caesars_intersection)
    print("DRAFTKINGS INTERSECTIONS -> " , draftkings_intersection)
    print("FANDUEL INTERSECTION-> ", fanduel_intersection)
    
    #Display open games as well as anchored games (Games that have a sofascore anchor as well as being on a sportsbook)

    with col1:
        st.header("Sofascore")
        for item in sorted(allSofascoreGamesDict.keys()):
            st.markdown(f"\t - {item}")
    with col2:
        st.header("Caesars")
        for item in sorted(allCaesarsGamesDict.keys()):
            st.markdown(f"\t - {item}")
        st.text("Anchored Games")
        st.write(list(caesars_intersection))
    with col3:
        st.header("Draftkings")
        for item in sorted(allDraftkingsGamesDict.keys()):
            st.markdown(f"\t - {item}")
        st.text("Anchored Games")
        st.write(list(draftkings_intersection))
    with col4:
        st.header("Fanduel")
        for item in sorted(allFanduelGamesDict.keys()):
            st.markdown(f"\t - {item}")
        st.text("Anchored Games")
        st.write(list(fanduel_intersection))

    #Attempting to display games states
    st.header("Current Game States")

    #Showing specific line comparisons
        #Dissecting what Set 1, Game 2, Point 3 winner is
        #Set 1 + Games 2 + Point 3

    st.header("Lines Covered - with Analysis")
    col1, col2, col3 = st.columns(3)
    with col1: 
        st.header("Caesars")
        print("Caesars Game Being Analyzed ...")
        with st.expander(f"Caesars Games"):
            for item in caesars_intersection:
                caesarsEvent = allCaesarsGamesDict[item]
                sofaScoreEvent = allSofascoreGamesDict[item]
                st.markdown(f'<h1 style="color:#FAF9F6;font-size:20px;"> Event Name: {item}</h1>', unsafe_allow_html=True)
                for caesars_game_line_key in caesarsEvent.game_lines:
                    caesars_game_line = caesarsEvent.game_lines[caesars_game_line_key]
                    game_state_glitch_check('caesars', sofaScoreEvent, caesars_game_line, item)
    with col2: 
        st.header("Draftkings")
        print("Draftkings Game Being Analyzed...")
        with st.expander(f"Draftkings Games"):
            for item in draftkings_intersection:
                draftkingsEvent = allDraftkingsGamesDict[item]
                sofaScoreEvent = allSofascoreGamesDict[item]
                st.markdown(f'<h1 style="color:#FAF9F6;font-size:20px;"> Event Name: {item}</h1>', unsafe_allow_html=True)
                for draftkings_game_line_key in draftkingsEvent.game_lines:
                    draftkings_game_line = draftkingsEvent.game_lines[draftkings_game_line_key]
                    game_state_glitch_check('draftkings', sofaScoreEvent, draftkings_game_line, item)
    with col3: 
        st.header("Fanduel")
        with st.expander(f"Fanduel Games"):
            for item in fanduel_intersection:
                print("fanduel Game Being Analyzed...", item)
                fanduelEvent = allFanduelGamesDict[item]
                sofaScoreEvent = allSofascoreGamesDict[item]
                st.markdown(f'<h1 style="color:#FAF9F6;font-size:20px;"> Event Name: {item}</h1>', unsafe_allow_html=True)
                for fanduel_game_line_key in fanduelEvent.game_lines:
                    fanduel_game_line = fanduelEvent.game_lines[fanduel_game_line_key]
                    game_state_glitch_check('fanduel', sofaScoreEvent, fanduel_game_line, item)


    st.write("Global glitches", global_glitches)
    print("global glitches length", len(global_glitches), global_glitches)
    if len(global_glitches) != 0:
        print("Data saved")
        utils.send_email(global_glitches)

    #Show the open game lines with no data analysis on them
    st.header('Covered Lines - No analysis')
    col1, col2, col3 = st.columns(3)
    def display_gameline_expander(sportsbook, sportsbookDict):
        with st.expander(f"{sportsbook} Games"):
            for key in sportsbookDict:
                st.markdown(f"Event name: {key}")
                for gameline in sportsbookDict[key].game_lines:
                    st.markdown(f"\t{gameline}")
    with col1: display_gameline_expander("Caesars", allCaesarsGamesDict)
    with col2: display_gameline_expander("Draftkings", allDraftkingsGamesDict)
    with col3: display_gameline_expander("Fanduel", allFanduelGamesDict)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("retrying in 5 seconds despite ", e)
        time.sleep(5)
        main()