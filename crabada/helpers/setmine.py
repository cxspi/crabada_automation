'''
Monitors the last when was the last mine started.
'''

import sys

sys.path.insert(0, 'C:')

import json
import time
import config

def read_json(path: str):
    with open(path) as json_file:
        data = json.load(json_file)
        return data

def write_json(path: str, data):
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def set_last_mine(public_a: str, json_path: str = config.addresses_file):
    data = read_json(json_path)

    data['addresses'][public_a]['last_mine'] = time.time()

    write_json(json_path, data)

if __name__ == '__main__':
    set_last_mine('0x')