#!/usr/bin/env python3

import json

# You can correlate these to the described methods on RhinoSecurityLabs.com
methods_and_permissions = {
    'UpdateIAMRole': [
        'iam.roles.update'
    ],
    'CreateServiceAccountKey': [
        'iam.serviceAccountKeys.create'
    ],
    'GetServiceAccountAccessToken': [
        'iam.serviceAccounts.getAccessToken'
    ],
    'ServiceAccountImplicitDelegation': [
        'iam.serviceAccounts.implicitDelegation'
    ],
    'ServiceAccountSignBlob': [
        'iam.serviceAccounts.signBlob'
    ],
    'ServiceAccountSignJwt': [
        'iam.serviceAccounts.signJwt'
    ],
    'SetOrgPolicyConstraints': [
        'orgpolicy.policy.set'
    ],
    'CreateServiceAccountHMACKey': [
        'storage.hmacKeys.create'
    ],
    'CreateDeploymentManagerDeployment': [
        'deploymentmanager.deployments.create'
    ],
    'RCECloudBuildBuildServer': [
        'cloudbuild.builds.create'
    ],
    'ExfilCloudFunctionCredsAuthCall': [
        'cloudfunctions.functions.create',
        'cloudfunctions.functions.sourceCodeSet',
        'iam.serviceAccounts.actAs',
        'cloudfunctions.functions.call'
    ],
    'ExfilCloudFunctionCredsUnauthCall': [
        'cloudfunctions.functions.create',
        'cloudfunctions.functions.sourceCodeSet',
        'iam.serviceAccounts.actAs',
        'cloudfunctions.functions.setIamPolicy'
    ],
    'UpdateCloudFunction': [
        'cloudfunctions.functions.sourceCodeSet',
        'cloudfunctions.functions.update',
        'iam.serviceAccounts.actAs'
    ],
    'CreateGCEInstanceWithSA': [
        'compute.disks.create',
        'compute.instances.create',
        'compute.instances.setMetadata',
        'compute.instances.setServiceAccount',
        'compute.subnetworks.use',
        'compute.subnetworks.useExternalIp',
        'iam.serviceAccounts.actAs'
    ],
    'ExfilCloudRunServiceUnauthCall': [
        'run.services.create',
        'iam.serviceaccounts.actAs',
        'run.services.setIamPolicy'
    ],
    'ExfilCloudRunServiceAuthCall': [
        'run.services.create',
        'iam.serviceaccounts.actAs',
        'run.routes.invoke'
    ],
    'CreateAPIKey': [
        'serviceusage.apiKeys.create'
    ],
    'ViewExistingAPIKeys': [
        'serviceusage.apiKeys.list'
    ],
    'SetOrgIAMPolicy': [
        'resourcemanager.organizations.setIamPolicy'
    ],
    'SetFolderIAMPolicy': [
        'resourcemanager.folders.setIamPolicy'
    ],
    'SetProjectIAMPolicy': [
        'resourcemanager.projects.setIamPolicy'
    ],
    'SetServiceAccountIAMPolicy': [
        'iam.serviceAccounts.setIamPolicy'
    ],
    'CreateCloudSchedulerHTTPRequest': [
        'cloudscheduler.jobs.create',
        'cloudscheduler.locations.list',
        'iam.serviceAccounts.actAs'
    ]
}


def check_privesc(permissions, resource_type, resource_id, member, f):
    print(f'{member} on {resource_type[:-1]} {resource_id}:')
    f.write(f'{member} on {resource_type[:-1]} {resource_id}:\n')
    for privesc_method in methods_and_permissions:
        if set(methods_and_permissions[privesc_method]).issubset(set(permissions)):
            print(f'    {privesc_method}')
            f.write(f'    {privesc_method}\n')

    f.write('\n')


# Output from enumerate_member_permissions.py
with open('all_org_folder_proj_sa_permissions.json', 'r') as f:
    permissions = json.load(f)

print('All Privilege Escalation Methods\n')
with open('privesc_methods.txt', 'w+') as f:
    for resource_type in permissions:  # Org, Folder, Proj, SA
        for resource in permissions[resource_type]:  # IDs of Orgs, Folders, Projs, SAs
            for member in permissions[resource_type][resource]:  # Members with permissions on the current resource
                check_privesc(permissions[resource_type][resource][member], resource_type, resource, member, f)

print('Misc. setIamPolicy Permissions\n')
with open('setIamPolicy_methods.txt', 'w+') as f:
    for resource_type in permissions:  # Org, Folder, Proj, SA
        for resource in permissions[resource_type]:  # IDs of Orgs, Folders, Projs, SAs
            for member in permissions[resource_type][resource]:  # Members with permissions on the current resource
                print(f'{member} on {resource_type[:-1]} {resource}:')
                f.write(f'{member} on {resource_type[:-1]} {resource}:\n')
                for permission in permissions[resource_type][resource][member]:
                    if 'setIamPolicy' in permission:
                        print(f'    {permission}')
                        f.write(f'    {permission}\n')

print('\nDone!')
print('Results output to ./privesc_methods.txt and ./setIamPolicy_methods.txt...')
