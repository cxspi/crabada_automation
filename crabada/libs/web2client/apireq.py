'''
This script handles all requests made to Crabada's server, and not to the blockchain. 
The only one at the moment is looking up crabs available in the tavern.
'''


import requests # type: ignore
import math
import json

HEADERS = {
            "authority": "idle-api.crabada.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "origin": "https://play.crabada.com",
            "pragma": "no-cache",
            "referer": "https://play.crabada.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36",
        }

def find_tavern_crabs():
        #time.sleep(2)
        
        try:
            response = requests.get("https://idle-game-api.crabada.com/public/idle/crabadas/lending?orderBy=time_point&order=desc&page=1&limit=100", headers=HEADERS, timeout=5)
            print(response.status_code)
        except Exception as e:
            print(e.__class__)
            print(e)
            return None

        if (response.status_code != 200):
            return None
        
        try:
            data = response.json()
        except Exception as e:
            print(e.__class__)
            print(e)
            return None

        return data


# Since there's only one request to handle I will process the data here.
# However, in case more functions are added move the data processing to a different file!




