#!/usr/bin/env python3
# Originally from https://medium.com/google-cloud/using-serviceaccountactor-iam-role-for-account-impersonation-on-google-cloud-platform-a9e7118480ed

PROJECT_ID = ''
TARGET_SERVICE_ACCOUNT = ''
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

from apiclient.discovery import build
import google.oauth2.credentials
import datetime, time, json, urllib, urllib.request

scope = 'https://www.googleapis.com/auth/iam https://www.googleapis.com/auth/cloud-platform'
credentials = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
service = build(serviceName='iam', version='v1', credentials=credentials)

expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=60)
expiration_time = int(time.mktime(expiration_time.timetuple()))
claim = json.dumps(
    {
        'iss': TARGET_SERVICE_ACCOUNT,
        'scope': scope,
        'aud': 'https://accounts.google.com/o/oauth2/token',
        'exp': expiration_time,
        'iat': expiration_time - 60
    }
)

slist = service.projects().serviceAccounts().signJwt(name=f'projects/{PROJECT_ID}/serviceAccounts/{TARGET_SERVICE_ACCOUNT}', body={'payload': claim})
resp = slist.execute()

signed_jwt = resp['signedJwt']

url = 'https://accounts.google.com/o/oauth2/token'
data = {
    'grant_type': 'assertion',
    'assertion_type': 'http://oauth.net/grant_type/jwt/1.0/bearer',
    'assertion': signed_jwt
}

headers = {'Content-type': 'application/x-www-form-urlencoded'}
data = urllib.parse.urlencode(data).encode()
req = urllib.request.Request(url, data, headers)
resp = urllib.request.urlopen(req).read()
parsed = json.loads(resp)
access_token = parsed.get('access_token')

print(access_token)
