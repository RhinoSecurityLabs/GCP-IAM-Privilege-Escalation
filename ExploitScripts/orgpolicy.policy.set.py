#!/usr/bin/env python3

ORG_ID = ''
FOLDER_ID = ''
PROJECT_ID = ''
CONSTRAINT_ID = 'constraints/appengine.disableCodeDownload'
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

from apiclient.discovery import build
import google.oauth2.credentials
import json

credentials = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
service = build(serviceName='cloudresourcemanager', version='v1', credentials=credentials)

body = {
    # Update depending on the constraint
    'policy': {
        'constraint': CONSTRAINT_ID,
        'booleanPolicy': {
            'enforced': False
        }
    }
}

# For Org-level
res = service.organizations().setOrgPolicy(resource=f'organizations/{ORG_ID}', body=body).execute()

# For Folder-level
# res = service.folders().setOrgPolicy(resource=f'folders/{FOLDER_ID}', body=body).execute()

# For Project-level
# res = service.projects().setOrgPolicy(resource=f'/projects/{PROJECT_ID}', body=body).execute()

print(json.dumps(res, indent=4))
