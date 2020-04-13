#!/usr/bin/env python3

PROJECT_ID = ''
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

from apiclient.discovery import build
import google.oauth2.credentials
import json

credentials = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
dm = build(serviceName='deploymentmanager', version='v2', credentials=credentials)

with open('./deploymentmanager.deployments.create-config.yaml', 'r') as f:
    config = f.read()

body = {
    'name': 'test-vm-deployment',
    'target': {
        'config': {
            'content': config
        }
    }
}

res = dm.deployments().insert(project=PROJECT_ID, body=body).execute()

print(json.dumps(res, indent=4))
