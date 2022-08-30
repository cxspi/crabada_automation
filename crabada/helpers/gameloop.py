import sys

sys.path.insert(0, r'C:')

from threading import Thread
import time
import json


import config
from crabada.helpers.setmine import set_last_mine
from crabada.helpers.reinforce import reinforcing_crab #type: ignore
from crabada.libs.web3client.txs.txs import Transacter, extract_pk #type: ignore
from crabada.libs.web3client.game import Team #type: ignore


import logging, logging.config

logging.config.fileConfig(config.loggerPath)
logger = logging.getLogger('sLogger')




# Eventually this won't be here:




address_file = config.addresses_file



# ^^^^^^^^ #


class gameLoopThread(Thread):
    def __init__(self, thread_team: Team):
        super().__init__()
        self.daemon = True
        self._running = True
        self.thread_team = thread_team
        self.transacter = Transacter()

    def game_loop(self, team: Team):
        with open(address_file) as json_file:
            data = json.load(json_file)


        print(team.teamId)
        # logger.info(f"Team: {team.teamId} still looping!")
        
        team.update_game_status()
        team.update_stats()
        
        
        if team.gameId == 0:
            if time.time() < data['addresses'][team.owner]['last_mine'] + (3.5*60*60)/data['addresses'][team.owner]['number_of_teams']:
                return

            print("Starting game!")
            # function to start game!
            print("Team owner:", team.owner)
            tx = self.transacter.start_game(team_id=team.teamId, public_a=team.owner, private_k=extract_pk(address_file, team.owner))
            team.update_game_status()
            logger.info(f"Team: {team.teamId} ; Started game: {team.gameId} ; Transaction: {tx}")
            set_last_mine(team.owner)
            
            return 

        if team.endTime < time.time():
            print("Closing game!")
            # function to close game!
            tx = self.transacter.close_game(game_id=team.gameId, public_a=team.owner, private_k=extract_pk(address_file, team.owner))
            logger.info(f"Team: {team.teamId} ; Ended game: {team.gameId} ; transaction {tx}")
            
            return

        if team.defId2 == 0:
            if team.lastAttackTime > team.lastDefTime and time.time() < (team.lastAttackTime + 30*60):
                print("Renting a crab!")
                crab = reinforcing_crab(team.owner)

                if crab == None:
                    print("Can't find a crab")
                    return

                tx = self.transacter.reinforce_defense(game_id=team.gameId, crabada_id = crab[0], borrow_price = crab[1],public_a=team.owner, private_k=extract_pk(address_file, team.owner))

                logger.info(f"Team: {team.teamId} ; Rented crab: {crab[0]} at {crab[1]} ; Transaction: {tx}")


    def run(self):
        print("Team number ", self.thread_team.teamId)
        while self._running:
            self.game_loop(self.thread_team)
            time.sleep(30)






