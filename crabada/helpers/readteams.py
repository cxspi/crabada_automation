''' 
File to read teams of the address' playing via the software from a google spread. 

Building an SQL database wouldn't be worth it. SQL DB would require developing a sort of 
admin panel for the client through Django or a different framework.
Google spreads offered a simple yet purposeful solution.  
'''
import sys
import time

sys.path.insert(0, r'C:')

from crabada.libs.web2client.quickstart import find_teams # type: ignore




def list_teams() -> list:
    teams = []

    # Each person who uses the software would get a spread, below are their id's
    spread_ids = [
        '...',
        '...',
        '...'
    ]


    for spread_id in spread_ids:
        values = find_teams(spread_id)

        if values == None:
            return None

        for count, item in enumerate(values[0]['values']):
            if not item:
                continue

            if not values[1]['values'][count] or values[1]['values'][count][0] != '1':
                continue

            teams.append(item[0])           

    return teams


if __name__ == '__main__':
    teams = list_teams()
    print(teams)
    print(len(teams))
    
    

