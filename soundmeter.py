#!/usr/bin/env python
# coding:utf-8

from apiclient import discovery
from datetime import date
from datetime import datetime
import oauth2client
import httplib2
import argparse
import subprocess
import json
import re
import time

# 変数定義
SPREADSHEET_ID = '12EpkVFzSDWzqdPuknacmKCKH9vu4Cn-ZqkCrJswPVdg'
MAJOR_DIMENSION = 'ROWS'
TIME_STAMP = int(time.time())
TODAY = str(datetime.fromtimestamp(TIME_STAMP)).split(' ')[0]
SHEET_NAME = TODAY
RANGE_NAME = 'A1'
SHEET_FLAG = 0
DURATION = '60'
 
CLIENT_SECRET_FILE = './client_secret.json'
CREDENTIAL_FILE = "./credential.json"
APPLICATION_NAME = 'Soundmeter Appender'

# 認証
store = oauth2client.file.Storage(CREDENTIAL_FILE)
credentials = store.get()
if not credentials or credentials.invalid:
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    args = '--auth_ht_name localht --logging_level INFO --noauth_local_webserver'
    flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args(args.split())
    credentials = oauth2client.tools.run_flow(flow, store, flags)
 
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?' 'version=v4')
service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
resource = service.spreadsheets().values()

# シートの名前を取得して、有り無しフラグの変更
sheet_meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
for sheet in sheet_meta.get('sheets', ''):
  # sheet名取得
  SHEET_TAB = sheet.get('properties', {}).get('title', 0)
  if TODAY == SHEET_TAB:
    SHEET_FLAG = 1

# シートがある場合は当日のシートで、ない場合はシート追加
if SHEET_FLAG == 1:
  SHEET_NAME = SHEET_TAB
else:
  BATCH_UPDATE_SPREADSHEET_REQUEST_BODY = {
    'requests': [
      {
        "addSheet": {
          "properties": {
            "title": TODAY
          }
        }
      }
    ]
  }
  service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=BATCH_UPDATE_SPREADSHEET_REQUEST_BODY).execute()

# soundmeterをコマンド実行
cmd = '/usr/local/bin/soundmeter -s' + DURATION
output = subprocess.getoutput(cmd)
jsonobj = {"data": []}

# soundmeter実行で得られた結果をjson変換
for line in output.split('\n'):
  m = line.split('\r')
  for e in m:
    dB = re.sub('[\s+]', '', e).replace('Timeout', '')
    if dB != '':
      jsonobj["data"].append([str(datetime.fromtimestamp(TIME_STAMP)),dB])
      TIME_STAMP += 1

# スプレッドシート追加データ形式に生成
BODY = {
  "range": SHEET_NAME + '!' + RANGE_NAME,
  "majorDimension": MAJOR_DIMENSION,
  "values": jsonobj["data"]
}

# スプレッドシートに追加
resource.append(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME + '!' + RANGE_NAME, valueInputOption='USER_ENTERED', body=BODY).execute()