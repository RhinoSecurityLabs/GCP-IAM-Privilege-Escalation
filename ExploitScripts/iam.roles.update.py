#!/usr/bin/env python3

# Project ID for project-level roles and Org ID for Organization-level roles
PROJECT_ID = ''
ORG_ID = ''
TARGET_ROLE_ID = ''
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

from apiclient.discovery import build
import google.oauth2.credentials
import json

credentials = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
service = build(serviceName='iam', version='v1', credentials=credentials)

body = {
    'includedPermissions': [
        'compute.instances.create'
        # Add more here
    ]
}

# If Project-level role
res = service.projects().roles().patch(name=f'projects/{PROJECT_ID}/roles/{TARGET_ROLE_ID}', body=body, updateMask='includedPermissions').execute()

# If Org-level role
# res = service.organizations().roles().patch(name=f'organizations/{ORG_ID}/roles/{TARGET_ROLE_ID}', body=body, updateMask='includedPermissions').execute()

print(json.dumps(res, indent=4))
