import asyncio
import json
import time

from web3.auto import w3, Web3 #type: ignore
from asgiref.sync import sync_to_async #type: ignore
from web3.middleware import geth_poa_middleware #type: ignore

w3 = Web3(Web3.HTTPProvider('https://rpc.swimmer.network/ext/bc/2K33xS9AyP9oCDiHYKVrHe7F54h2La5D8erpTChaAhdzeSu2RX/rpc'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(w3.isConnected())
CRABADA_CONTRACT = "0x"
CRABADA_ABI = json.load(open(r'0x0x', 'r'))

contract = w3.eth.contract(address=CRABADA_CONTRACT, abi=CRABADA_ABI)
tx = contract.functions.getCrab(105070).call() #buildTransaction({'from': "0x"})
print(tx)



