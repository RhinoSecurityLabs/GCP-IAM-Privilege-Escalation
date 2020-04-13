#!/usr/bin/env python3
# Originally from https://github.com/salrashid123/gcpsamples/tree/master/gcs_keyless_signedurl

TARGET_SERVICE_ACCOUNT = ''
BUCKET_NAME = ''
OBJECT_NAME = ''
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

import time

from apiclient.discovery import build
import google.oauth2.credentials

import base64
import datetime
import urllib
import requests

credentials = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
expiration = datetime.datetime.now() + datetime.timedelta(seconds=60)
expiration = int(time.mktime(expiration.timetuple()))


def _Base64Sign(plaintext):
    project_id = '-'

    iamcredentials = build(serviceName='iamcredentials', version='v1', credentials=credentials)
    body = {
        'delegates': [],
        'payload': base64.urlsafe_b64encode(plaintext.encode()).decode('utf-8')
    }
    req = iamcredentials.projects().serviceAccounts().signBlob(name=f'projects/{project_id}/serviceAccounts/{TARGET_SERVICE_ACCOUNT}', body=body)
    resp = req.execute()
    return resp['signedBlob']


def _MakeSignatureString(verb, path, content_md5, content_type):
    signature_string = ('{verb}\n'
                        '{content_md5}\n'
                        '{content_type}\n'
                        '{expiration}\n'
                        '{resource}')
    return signature_string.format(
        verb=verb,
        content_md5=content_md5,
        content_type=content_type,
        expiration=expiration,
        resource=path
    )


def MakeUrl(verb, path, content_type='', content_md5=''):
    signature_string = _MakeSignatureString(verb, path, content_md5, content_type)
    signature_signed = urllib.parse.quote(_Base64Sign(signature_string))

    signed_url = 'https://storage.googleapis.com/' + \
        BUCKET_NAME + '/' + OBJECT_NAME + '?GoogleAccessId=' + \
        TARGET_SERVICE_ACCOUNT + '&Expires=' + str(expiration) + \
        '&Signature=' + signature_signed

    return signed_url


file_path = '/%s/%s' % (BUCKET_NAME, OBJECT_NAME)


# print('PUT:')
# u =  MakeUrl('PUT',file_path)
# print(u)
# r = requests.put(u, data='lorem2 ipsum')
# print('PUT status_code: ' + str(r.status_code))

# print('---------------------------------')

print('GET')
u = MakeUrl('GET', file_path)
print(u)
r = requests.get(u)
print('GET status_code: ' + str(r.status_code))
print('Data: ' + r.text)
