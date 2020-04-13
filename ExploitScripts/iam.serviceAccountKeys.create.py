#!/usr/bin/env python3

PROJECT_ID = ''
TARGET_SERVICE_ACCOUNT = ''
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

from apiclient.discovery import build
import google.oauth2.credentials
import json

credentials = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
service = build(serviceName='iam', version='v1', credentials=credentials)

res = service.projects().serviceAccounts().keys().create(name=f'projects/{PROJECT_ID}/serviceAccounts/{TARGET_SERVICE_ACCOUNT}', body={}).execute()

print(json.dumps(res, indent=4))
