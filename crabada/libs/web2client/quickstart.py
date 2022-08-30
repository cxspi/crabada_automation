'''
Connects to the Google API to access the spreads.
'''

from googleapiclient.errors import HttpError # type: ignore
from googleapiclient.discovery import build # type: ignore
from google.oauth2 import service_account # type: ignore
import config

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = config.googleSheetsJsonPath

range_names = [
    'teams!A2:A1000',
    'teams!B2:B1000'
]

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def find_teams(spread_id):
    try:
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        result = sheet.values().batchGet(
            spreadsheetId=spread_id, ranges=range_names).execute()
        ranges = result.get('valueRanges', [])

        return ranges

    except HttpError as err:
        print(err)
        return None

    except TimeoutError as err:
        print(err)
        return None

if __name__ == '__main__':
    #main()
    pass