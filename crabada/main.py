'''
'main' brings all of the scripts above together, and runs the main game loop. 
It is short but ensures all systems are working correctly. 
'''

import sys

sys.path.insert(0, 'C:')
sys.path.insert(0, 'C:')

import time
from threading import Thread, active_count

import helpers.teamsmanagement as tmgt
from helpers.readteams import list_teams
from helpers.gameloop import gameLoopThread
from libs.web3client.game import Team
from libs.web3client.txs.txs import Transacter









def main():
    available_teams = list_teams()    
    teams = {team_id:Team(int(team_id)) for team_id in available_teams}
    # gameLoopThreads = {team:gameLoopThread(Team(int(team))) for team in available_teams}
    gameLoopThreads = dict()
    print(gameLoopThreads.keys())

    count = 1
    while True:
        if count % 60 == 0:
            print("Updating teams!")
            result = list_teams() 
            print(result)
            if result != None:
                available_teams = result

        print(len(available_teams))
        print(active_count() - 1)

        # Handler if team count has changes:
        tmgt.handle_add_remove(available_teams, gameLoopThreads)


        # When a thread fails, it restarts it! (technically replaces it) 
        # TODO : add error handling :/
        for key in gameLoopThreads:
            if gameLoopThreads[key].is_alive() == False:
                print(gameLoopThreads[key], 'is down.', key)
                gameLoopThreads.update({key: gameLoopThread(Team(int(key)))})

                gameLoopThreads[key].start()

        count += 1
        time.sleep(2)






if __name__ == '__main__':
    main()