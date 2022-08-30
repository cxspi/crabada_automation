from web3 import Web3 #type: ignore
import web3 #type: ignore
from web3.middleware import geth_poa_middleware #type: ignore
import json
import config

def extract_pk(path, public_a):
    with open (path) as json_file:
        data = json.load(json_file)
        pk = data["addresses"][public_a]['pk']
        
        return pk

class Transacter():
    '''
    Introducing, the Transacter. They know where to connect, which contract, which network and how. 
    Your job is to put your request and they will do it for you! 

    e.g 

    Transacter.startGame(team_id)
    '''
    def __init__(self) -> None:
        self.w3 = Web3(Web3.HTTPProvider(config.swimmerHttp))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.chainId = config.swimmerChainId
        self.lower_case_address = config.idleGameContract
        self.CRABADA_CONTRACT = Web3.toChecksumAddress(self.lower_case_address)
        self.CRABADA_ABI = json.load(open(config.idleGameABI, 'r'))
        self.contract = self.w3.eth.contract(address=self.CRABADA_CONTRACT, abi=self.CRABADA_ABI)
    
    def transaction_dic(self, public_a):
        tx = {
            'from': public_a,
            'nonce': self.w3.eth.get_transaction_count(public_a),
            'chainId': self.chainId,
        }

        return tx

    def send_tx(self, transaction, private_k):

        signed_tx = self.w3.eth.account.sign_transaction(transaction, private_k)

        try:
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        except:
            return

        try:
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout = 300)
        except web3.exceptions.TransactionNotFound:
            pass
        
        # TODO: Replace with logging 
        
        if receipt['status'] == 1:
            print("Success!")
        if receipt['status'] == 0:
            print("Failed!")

        return tx_hash

    def start_game(self, team_id, public_a, private_k):
        tx = self.contract.functions.startGame(team_id).buildTransaction(self.transaction_dic(public_a))
        print(tx)
        tx_hash = self.send_tx(tx, private_k)
        return tx_hash

    def close_game(self, game_id, public_a, private_k):
        tx = self.contract.functions.closeGame(game_id).buildTransaction(self.transaction_dic(public_a))
        print(tx)
        tx_hash = self.send_tx(tx, private_k)
        return tx_hash

        
    def reinforce_defense(self, game_id, crabada_id, borrow_price, public_a, private_k):
        tx_dic = self.transaction_dic(public_a)
        tx_dic['value'] = borrow_price
        tx = self.contract.functions.reinforceDefense(game_id, crabada_id, borrow_price).buildTransaction(tx_dic)

        if tx['gas'] * Web3.fromWei(tx['maxFeePerGas'], 'ether') > 20:
            print("Gas too high!")
            return None

        print(tx)

        tx_hash = self.send_tx(tx, private_k)
        return tx_hash


if __name__ == '__main__':
    address_file = config.addresses_file
    print(extract_pk(address_file, "0x"))


