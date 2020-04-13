#!/usr/bin/env python3

# Use the GCP web console to request HMAC keys for a regular user (not a Service Account)

PROJECT_ID = ''
TARGET_SERVICE_ACCOUNT = ''
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

import requests
import json

key = requests.post(
    f'https://www.googleapis.com/storage/v1/projects/{PROJECT_ID}/hmacKeys',
    params={'access_token': ACCESS_TOKEN, 'serviceAccountEmail': TARGET_SERVICE_ACCOUNT}
).json()

print(json.dumps(key, indent=4))
