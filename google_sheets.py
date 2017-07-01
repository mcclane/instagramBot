from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Instagram Data Logger'
spreadsheetId = '1J9qsZZkTunp-QQGOQtPmd-kEbjJ4w5nqu1s9lyV-xM4'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


####################################################################
#set up the thing, which is pretty important
####################################################################
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)


def upload(data, rangeName='Sheet1!A:C'):
    value_input_option = "USER_ENTERED"
    insert_data_option = "INSERT_ROWS"
    value_range_body = {
        "values": data
    }
    request = service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=rangeName, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()
    #print(response)
