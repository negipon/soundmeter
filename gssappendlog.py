#!/usr/bin/env python
# coding:utf-8
from apiclient import discovery
import oauth2client
import httplib2
import argparse
import csv
import sys
import os
 
SPREADSHEET_ID = '12EpkVFzSDWzqdPuknacmKCKH9vu4Cn-ZqkCrJswPVdg'
RANGE_NAME = 'A1'
MAJOR_DIMENSION = 'ROWS'
 
CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIAL_FILE = "./credential.json"
APPLICATION_NAME = 'CSV Appender'
 
store = oauth2client.file.Storage(CREDENTIAL_FILE)
credentials = store.get()
if not credentials or credentials.invalid:
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    args = '--auth_host_name localhost --logging_level INFO --noauth_local_webserver'
    flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args(args.split())
    credentials = oauth2client.tools.run_flow(flow, store, flags)
 
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
resource = service.spreadsheets().values()
 
parser = argparse.ArgumentParser()
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin)
args = parser.parse_args(sys.argv[1:])
 
r = csv.reader(args.infile, delimiter=' ')
data = list(r)


body = {
    "range": RANGE_NAME,
    "majorDimension": MAJOR_DIMENSION,
    "values": data
}

print (body)

resource.append(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
                valueInputOption='USER_ENTERED', body=body).execute()

os.remove(sys.argv[1])

try:
    os.system('soundmeter --seconds 10 --log meter.log')
except:
    print ('Error.')