

#testing full async call load

from sofascoreParser import *
import caesarsParser as caesarsParser
import draftkingsParser as draftkingsParser
import fanduelParser as fanduelParser
import mgmParser as mgmParser
import sofascoreParser as sofascoreParser
import betriversParser as betriversParser
import barstoolsParser as barstoolsParser
import twinspiresParser as twinspiresParser
import unibetParser as unibetParser
import time

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, thread

allSofascoreGamesDict = {}
allCaesarsGamesDict = {} 
allDraftkingsGamesDict = {}
allFanduelGamesDict = {}
allMgmGamesDict = {}
allBetriversGamesDict = {} 
allBarstoolsGamesDict = {}
allTwinspiresGamesDict = {}
allUnibetGamesDict = {}

def thread_pool_executor():
    global allCaesarsGamesDict
    global allDraftkingsGamesDict
    global allFanduelGamesDict
    global allMgmGamesDict
    global allSofascoreGamesDict
    global allBetriversGamesDict
    global allBarstoolsGamesDict
    global allTwinspiresGamesDict
    global allUnibetGamesDict

    res = [] 
    def aggregated_run_full_test_code(sportsbook):
        save_json = ''
        if sportsbook == 'caesars':
            global allCaesarsGamesDict
            allCaesarsGamesDict =  caesarsParser.test_full_code("online") 
            save_json = allCaesarsGamesDict
        elif sportsbook == 'draftkings':
            global allDraftkingsGamesDict
            allDraftkingsGamesDict =  draftkingsParser.test_full_code("online")
            save_json = allDraftkingsGamesDict
        elif sportsbook == 'fanduel':
            global allFanduelGamesDict
            allFanduelGamesDict =  fanduelParser.test_full_code("online")
            save_json = allFanduelGamesDict
        elif sportsbook == 'mgm':
            global allMgmGamesDict
            allMgmGamesDict =  mgmParser.test_full_code("online")
            save_json = allMgmGamesDict
        elif sportsbook == 'betrivers':
            global allBetriversGamesDict
            allBetriversGamesDict =  betriversParser.test_full_code("online")
            save_json = allBetriversGamesDict
        elif sportsbook == 'sofascore':
            global allSofascoreGamesDict
            allSofascoreGamesDict = sofascoreParser.test_full_code('online')
            save_json = allSofascoreGamesDict
        elif sportsbook == 'barstools':
            global allBarstoolsGamesDict
            allBarstoolsGamesDict = barstoolsParser.test_full_code('online')
            save_json = allBarstoolsGamesDict
        elif sportsbook == 'twinspires':
            global allTwinspiresGamesDict
            allTwinspiresGamesDict = twinspiresParser.test_full_code('online')
            save_json = allTwinspiresGamesDict
        elif sportsbook == 'unibet':
            global allUnibetGamesDict
            allUnibetGamesDict = unibetParser.test_full_code('online')
            save_json = allUnibetGamesDict
        return save_json

    #CODE WRITE UP
    executor = ThreadPoolExecutor(max_workers=10)
    my_items = ['caesars', 'draftkings', 'fanduel', 'mgm', 'betrivers','sofascore', 'barstools', 'twinspires', 'unibet']
    for result in executor.map(aggregated_run_full_test_code, my_items):
        pass
    #print(allSofascoreGamesDict, allCaesarsGamesDict, allDraftkingsGamesDict, allFanduelGamesDict, allMgmGamesDict)
    executor.shutdown(wait=True, cancel_futures=False)
    return allSofascoreGamesDict, allCaesarsGamesDict, allDraftkingsGamesDict, allFanduelGamesDict, allMgmGamesDict, allBetriversGamesDict, allBarstoolsGamesDict, allTwinspiresGamesDict, allUnibetGamesDict

def main():
    start_time = time.time()
    thread_pool_executor()
    end_time = time.time() - start_time
    print("time elapsed ->", end_time)

if __name__ == "__main__":
    main()