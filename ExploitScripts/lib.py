from apiclient.discovery import build
import json

def select(msg, choices):
    for i, value in enumerate(choices):
        print(f"{i}) {value['name']}")

    selection = None
    while not selection:
        index = input(msg)
        try:
            selection = choices[int(index)]
        except ValueError:
            continue
    return selection

def select_project(creds):
    mgr = build(serviceName='cloudresourcemanager', version='v1', credentials=creds)
    projects = mgr.projects().list().execute()['projects']
    return select('Select project: ', projects)


def select_svc_account(creds, project):
    iam = build(serviceName='iam', version='v1', credentials=creds)
    svc_accounts = iam.projects().serviceAccounts().list(name=f"projects/{project}").execute()
    return select('Select service account: ', svc_accounts['accounts'])
