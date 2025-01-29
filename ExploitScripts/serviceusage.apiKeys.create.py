#!/usr/bin/env python3

import json
import requests
import google.oauth2.credentials
import time

import lib

from apiclient.discovery import build

PROJECT_ID = ''
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()


creds = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
apikeys = build(serviceName='apikeys', version='v2', credentials=creds)

project = lib.select_project(creds)

resp = apikeys.projects().locations().keys().create(parent=f"projects/{project['projectId']}/locations/global").execute()

while not resp.get('done'):
    resp = apikeys.operations().get(name=resp['name']).execute()
    print('.', end='', flush=True)
    time.sleep(1)

print(json.dumps(resp, indent=4))
