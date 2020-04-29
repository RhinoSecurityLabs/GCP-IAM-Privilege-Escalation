#!/usr/bin/env python3
# Originally from https://medium.com/google-cloud/using-serviceaccountactor-iam-role-for-account-impersonation-on-google-cloud-platform-a9e7118480ed

PROJECT_ID = ''
TARGET_SERVICE_ACCOUNT = ''
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

import google.oauth2.credentials
from apiclient.discovery import build
import base64, urllib, urllib.request, json, time
scope = 'https://www.googleapis.com/auth/iam https://www.googleapis.com/auth/cloud-platform'
credentials = google.oauth2.credentials.Credentials(ACCESS_TOKEN)

service = build(serviceName='iam', version='v1', credentials=credentials)
resource = service.projects()


def _urlsafe_b64encode(raw_bytes):
    return base64.urlsafe_b64encode(raw_bytes).decode().rstrip('=')


def _urlsafe_b64decode(b64string):
    b64string = b64string.encode('ascii')
    padded = b64string + '=' * (4 - len(b64string) % 4)
    return base64.urlsafe_b64decode(padded)


jwt_header = '{"alg":"RS256","typ":"JWT"}'.encode()
jwt_scope = scope  # 'https://www.googleapis.com/auth/userinfo.email'

iss = TARGET_SERVICE_ACCOUNT
now = int(time.time())
exptime = now + 3600
claim = (
            '{"iss":"%s",'
            '"scope":"%s",'
            '"aud":"https://accounts.google.com/o/oauth2/token",'
            '"exp":%s,'
            '"iat":%s}'
        ) % (iss,jwt_scope,exptime,now)

jwt = _urlsafe_b64encode(jwt_header) + '.' + _urlsafe_b64encode(claim.encode())

slist = resource.serviceAccounts().signBlob(name=f'projects/{PROJECT_ID}/serviceAccounts/{TARGET_SERVICE_ACCOUNT}', body={'bytesToSign': base64.b64encode(jwt.encode()).decode()})

resp = slist.execute()
r = _urlsafe_b64encode(base64.decodebytes(resp['signature'].encode()))
signed_jwt = jwt + '.' + r

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
print('access_token: ' + access_token)
