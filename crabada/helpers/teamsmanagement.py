'''
Each team follows a different cycle with different times. 
They should not interfere or be depedent on each other. 
Each tread represents a team, and runs the game loop for it.
'''

# TODO 

# Add error handling :')

import sys
sys.path.insert(0, r'C:')

from crabada.helpers.gameloop import gameLoopThread
from crabada.libs.web3client.game import Team # type: ignore

def difference_between(list_a, list_b):
    difference = [element for element in list_a if element not in list_b]
    return difference

def addThreads(teams, add_to: dict):
    for team in teams:
        add_to[team] = gameLoopThread(Team(int(team)))
        add_to[team].start()

def removeThreads(teams, remove_from: dict):
    for team in teams:
        remove_from[team]._running = False
        remove_from[team].join() 
        remove_from.pop(team)

def handleAddition(list_a, dict_b):
    difference = difference_between(list_a, dict_b.keys())
    addThreads(teams = difference, add_to = dict_b)

def handleSubstraction(list_a, dict_b):
    difference = difference_between(dict_b.keys(), list_a)
    removeThreads(teams = difference, remove_from=dict_b)

def handle_add_remove(list_a, dict_b):
    if len(list_a) > len(dict_b): # Checking if teams were added
        print('Added teams')
        handleAddition(list_a, dict_b)
        print(dict_b.keys())

    if len(list_a) < len(dict_b): # Checking if teams were removed
        print('Removed teams')
        handleSubstraction(list_a, dict_b)
        print(dict_b.keys())