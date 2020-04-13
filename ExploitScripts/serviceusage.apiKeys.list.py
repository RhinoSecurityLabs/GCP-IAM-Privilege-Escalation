#!/usr/bin/env python3

PROJECT_ID = ''
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

import requests
import json

keys = requests.get(
    f'https://apikeys.googleapis.com/v1/projects/{PROJECT_ID}/apiKeys',
    params={'access_token': ACCESS_TOKEN}
).json()

print(json.dumps(keys, indent=4))
