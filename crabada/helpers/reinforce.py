'''
This script controls the reinforcement process of the game.
It finds the cheapest most efficient Crab to use. 
'''

from distutils.command import check
import sys
sys.path.insert(0, 'C:')

import json
import math
import time

import config
import crabada.libs.web3client.game as game
import crabada.libs.web2client.apireq as apireq

def fetch_tavern_crabs():
        crabs = []

        data = apireq.find_tavern_crabs()
        if data != None:
            data = data['result']['data']
            # print(data)
            for i in data:
                if i["mine_point"] == None or i['price'] == None:
                    break

                if i["mine_point"] > 80 and i['price'] < 150 * (10 ** 18) :
                    crabs.append((i['crabada_id'], i['price'], i['class_name']))

        if crabs != []:
            return crabs[math.ceil(len(crabs)/2)-1]
        else: 
            return None

# < -------------------------------------------------------------------------- > #

def fetch_inventory_crabs(public_a, path = config.addresses_file) -> list:
    with open (path) as json_file:
        data = json.load(json_file)
        crabs = data["addresses"][public_a]['available_crabs']

        return crabs

def check_inventory_crabs(public_a, path = config.addresses_file) -> list:
    crabs = fetch_inventory_crabs(public_a, path)

    for crab in crabs:
        _crab = game.getCrab(crab)
        if _crab[1] < time.time() and _crab[2] == 0:
            return (crab, 0)
        
    return None

def reinforcing_crab(public_a, path = config.addresses_file):
    inv_crab = check_inventory_crabs(public_a, path)

    if inv_crab != None:
        print(inv_crab)
        return inv_crab
    
    tav_crab = fetch_tavern_crabs()
    return tav_crab




if __name__ == '__main__':
    print(1)
    print(reinforcing_crab("0x"))
    
