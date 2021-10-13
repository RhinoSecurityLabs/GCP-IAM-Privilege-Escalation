#!/usr/bin/env python3

ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

from apiclient.discovery import build
import google.oauth2.credentials
import json

import lib


def select(msg, choices):
    for i, value in enumerate(choices):
        print(f"{i}) {value['name']}")

    selection = None
    while not selection:
        index = input(msg)
        try:
            selection = choices[int(index)]
        except ValueError:
            continue
    return selection

creds = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
service = build(serviceName='iamcredentials', version='v1', credentials=creds)

project = lib.select_project(creds)
svc_account = lib.select_svc_account(creds, project['projectId'])

body = {
    'scope': [
        'https://www.googleapis.com/auth/iam',
        'https://www.googleapis.com/auth/cloud-platform'
    ]
}

res = service.projects().serviceAccounts().generateAccessToken(name=f'projects/-/serviceAccounts/{svc_acccount["email"]}', body=body).execute()

print(json.dumps(res, indent=4))
