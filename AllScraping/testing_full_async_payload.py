

#testing full async call load

from sofascoreParser import *
import caesarsParser as caesarsParser
import draftkingsParser as draftkingsParser
import fanduelParser as fanduelParser
import mgmParser as mgmParser
import time

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, thread


# def main():
#     allSofascoreGamesDict,   allCaesarsGamesDict,   allDraftkingsGamesDict, allFanduelGamesDict, allMgmGamesDict = [] , [], [], [], []
#     def aggregated_run_full_test_code(sportsbook):
#         save_json = ''
#         if sportsbook == 'caesars':
#             allCaesarsGamesDict =  caesarsParser.test_full_code("online") 
#             save_json = allCaesarsGamesDict
#         elif sportsbook == 'draftkings':
#             allDraftkingsGamesDict =  draftkingsParser.test_full_code("online")
#             save_json = allDraftkingsGamesDict
#         elif sportsbook == 'fanduel':
#             allFanduelGamesDict =  fanduelParser.test_full_code("online")
#             save_json = allFanduelGamesDict
#         elif sportsbook == 'mgm':
#             allMgmGamesDict =  mgmParser.test_full_code("online")
#             save_json = allMgmGamesDict
#         return save_json
#     thread1 = threading.Thread(target=aggregated_run_full_test_code, args=("caesars", ))
#     thread2 = threading.Thread(target=aggregated_run_full_test_code, args=("draftkings", ))
#     thread3 = threading.Thread(target=aggregated_run_full_test_code, args=("fanduel", ))
#     thread4 = threading.Thread(target=aggregated_run_full_test_code, args=("mgm", ))

#     thread1.start()
#     thread2.start()
#     thread3.start()
#     thread4.start()

#     thread1.join()
#     thread2.join()
#     thread3.join()
#     thread4.join()

    # print(allSofascoreGamesDict != None)
    
def thread_pool_executor():
    res = [] 
    def aggregated_run_full_test_code(sportsbook):
        save_json = ''
        if sportsbook == 'caesars':
            allCaesarsGamesDict =  caesarsParser.test_full_code("online") 
            save_json = allCaesarsGamesDict
        elif sportsbook == 'draftkings':
            allDraftkingsGamesDict =  draftkingsParser.test_full_code("online")
            save_json = allDraftkingsGamesDict
        elif sportsbook == 'fanduel':
            allFanduelGamesDict =  fanduelParser.test_full_code("online")
            save_json = allFanduelGamesDict
        elif sportsbook == 'mgm':
            allMgmGamesDict =  mgmParser.test_full_code("online")
            save_json = allMgmGamesDict
        return save_json
    
    #CODE WRITE UP
    executor = ThreadPoolExecutor(max_workers=10)
    my_items = ['caesars', 'draftkings', 'fanduel', 'mgm']
    for result in executor.map(aggregated_run_full_test_code, my_items):
	    print('Submited execution to threadpool') 

start_time = time.time()
thread_pool_executor()
end_time = time.time() - start_time
print("time elapsed ->", end_time)


