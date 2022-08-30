import sys

sys.path.insert(0, 'C:')


from dataclasses import dataclass
import json
import time

import config
from web3.auto import w3, Web3 #type: ignore
from web3.middleware import geth_poa_middleware #type: ignore

# TODO 
# Remove web3 configurations to requirements file (i think) and set path here

w3 = Web3(Web3.HTTPProvider(config.swimmerHttp))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

lower_case_address = config.idleGameContract
CRABADA_IDLE_CONTRACT = Web3.toChecksumAddress(lower_case_address)

CRABADA_IDLE_ABI = json.load(open(config.idleGameABI, 'r'))

contract = w3.eth.contract(address=CRABADA_IDLE_CONTRACT, abi=CRABADA_IDLE_ABI)


CRABADA_DATA_ABI = json.load(open(config.crabadaDataABI))
crab_contract = w3.eth.contract(address=config.crabadaDataContract, abi=CRABADA_DATA_ABI)




def getTeamInfo(teamId: int) -> list:
    info = contract.functions.getTeamInfo(teamId).call() 
    return teamId, info

def getCrab(crabadaId: int) -> list:
    info = crab_contract.functions.getCrab(crabadaId).call()
    return info


@dataclass
class Team():
    '''Game represent a game instance of a certain team.
    
        This class does not process any transactions, only informs the script whether a transaction should be made
        e.g. closeGame(), reinforceDefense()...
    '''
    owner = 0
    teamId: int
    # Basic game values
    gameId: int = 0
    craReward: int = 0
    tusReward: int = 0
    startTime: int = 0
    duration: int = 0
    endTime: int = startTime + duration
    status: int = 0
    # Battle values
    attackTeamId: int = 0
    attackTime: int = 0
    lastAttackTime: int = 0
    lastDefTime: int = 0
    attackId1: int = 0
    attackId2: int = 0
    defId1: int = 0
    defId2: int = 0


    def getGameBasicInfo(self) -> list:
        try:
            info = contract.functions.getGameBasicInfo(self.gameId).call()
        except:
            return None
        return info

    def getGameBattleInfo(self) -> list:
        try:
            info = contract.functions.getGameBattleInfo(self.gameId).call() 
        except: 
            return None
        return info


    def getTeamInfo(self) -> list:
        try:
            info = contract.functions.getTeamInfo(self.teamId).call()
        except:
            return None
        return info


    def update_game_status(self):
        info = self.getTeamInfo()
        if info == None:
            return
        self.owner, self.gameId = info[0], info[-2]

    def update_stats(self):
        basic_values = self.getGameBasicInfo()
        battle_values = self.getGameBattleInfo()

        if basic_values == None or battle_values == None:
            return None

        self.craReward, self.tusReward, self.startTime, self.duration, self.status = (value for value in basic_values[1:])
        self.attackTeamId, self.attackTime, self.lastAttackTime, self.lastDefTime, self.attackId1, self.attackId2, self.defId1, self.defId2 = (value for value in battle_values)
        self.endTime = self.startTime + self.duration




if __name__ == '__main__':
    team = Team(00000)
    team.update_game_status()
    print(team.owner)

    crab = getCrab(00000)
    print(crab)

