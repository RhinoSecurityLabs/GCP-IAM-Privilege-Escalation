#!/usr/bin/env python3

import sys
import json

# You can correlate these to the described methods here: https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/ and here: https://rhinosecuritylabs.com/cloud-security/privilege-escalation-google-cloud-platform-part-2/
methods_and_permissions = {
    'UpdateIAMRole': {
        'Permissions': [
            'iam.roles.update'
        ],
        'Scope': [
            'Organization',
            'Project'
        ]
    },
    'CreateServiceAccountKey': {
        'Permissions': [
            'iam.serviceAccountKeys.create'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project',
            'ServiceAccount'
        ]
    },
    'GetServiceAccountAccessToken': {
        'Permissions': [
            'iam.serviceAccounts.getAccessToken'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project',
            'ServiceAccount'
        ]
    },
    'ServiceAccountImplicitDelegation': {
        'Permissions': [
            'iam.serviceAccounts.implicitDelegation'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project',
            'ServiceAccount'
        ]
    },
    'ServiceAccountSignBlob': {
        'Permissions': [
            'iam.serviceAccounts.signBlob'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project',
            'ServiceAccount'
        ]
    },
    'ServiceAccountSignJwt': {
        'Permissions': [
            'iam.serviceAccounts.signJwt'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project',
            'ServiceAccount'
        ]
    },
    'SetOrgPolicyConstraints': {
        'Permissions': [
            'orgpolicy.policy.set'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'CreateServiceAccountHMACKey': {
        'Permissions': [
            'storage.hmacKeys.create'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project',
            'ServiceAccount'
        ]
    },
    'CreateDeploymentManagerDeployment': {
        'Permissions': [
            'deploymentmanager.deployments.create'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'RCECloudBuildBuildServer': {
        'Permissions': [
            'cloudbuild.builds.create'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'ExfilCloudFunctionCredsAuthCall': {
        'Permissions': [
            'cloudfunctions.functions.create',
            'cloudfunctions.functions.sourceCodeSet',
            'iam.serviceAccounts.actAs',
            'cloudfunctions.functions.call'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'ExfilCloudFunctionCredsUnauthCall': {
        'Permissions': [
            'cloudfunctions.functions.create',
            'cloudfunctions.functions.sourceCodeSet',
            'iam.serviceAccounts.actAs',
            'cloudfunctions.functions.setIamPolicy'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'UpdateCloudFunction': {
        'Permissions': [
            'cloudfunctions.functions.sourceCodeSet',
            'cloudfunctions.functions.update',
            'iam.serviceAccounts.actAs'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'CreateGCEInstanceWithSA': {
        'Permissions': [
            'compute.disks.create',
            'compute.instances.create',
            'compute.instances.setMetadata',
            'compute.instances.setServiceAccount',
            'compute.subnetworks.use',
            'compute.subnetworks.useExternalIp',
            'iam.serviceAccounts.actAs'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'ExfilCloudRunServiceUnauthCall': {
        'Permissions': [
            'run.services.create',
            'iam.serviceaccounts.actAs',
            'run.services.setIamPolicy'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'ExfilCloudRunServiceAuthCall': {
        'Permissions': [
            'run.services.create',
            'iam.serviceaccounts.actAs',
            'run.routes.invoke'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'CreateAPIKey': {
        'Permissions': [
            'serviceusage.apiKeys.create'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'ViewExistingAPIKeys': {
        'Permissions': [
            'serviceusage.apiKeys.list'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'SetOrgIAMPolicy': {
        'Permissions': [
            'resourcemanager.organizations.setIamPolicy'
        ],
        'Scope': [
            'Organization'
        ]
    },
    'SetFolderIAMPolicy': {
        'Permissions': [
            'resourcemanager.folders.setIamPolicy'
        ],
        'Scope': [
            'Organization',
            'Folder'
        ]
    },
    'SetProjectIAMPolicy': {
        'Permissions': [
            'resourcemanager.projects.setIamPolicy'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    },
    'SetServiceAccountIAMPolicy': {
        'Permissions': [
            'iam.serviceAccounts.setIamPolicy'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project',
            'ServiceAccount'
        ]
    },
    'CreateCloudSchedulerHTTPRequest': {
        'Permissions': [
            'cloudscheduler.jobs.create',
            'cloudscheduler.locations.list',
            'iam.serviceAccounts.actAs'
        ],
        'Scope': [
            'Organization',
            'Folder',
            'Project'
        ]
    }
}


def check_privesc(permissions, resource_type, resource_id, member, f):
    first_method = True
    for privesc_method in methods_and_permissions:
        if set(methods_and_permissions[privesc_method]['Permissions']).issubset(set(permissions)) and resource_type[:-1] in methods_and_permissions[privesc_method]['Scope']:
            if first_method:  # Only print out a user if there is a method associated with it
                print(f'{member} on {resource_type[:-1]} {resource_id}:')
                f.write(f'{member} on {resource_type[:-1]} {resource_id}:\n')
                first_method = False
            print(f'    {privesc_method}')
            f.write(f'    {privesc_method}\n')

    if first_method is False:
        f.write('\n')


try:
    # Output from enumerate_member_permissions.py
    with open('all_org_folder_proj_sa_permissions.json', 'r') as f:
        permissions = json.load(f)
except FileNotFoundError:
    print('Could not find all_org_folder_proj_sa_permissions.json. Run "enumerate_member_permissions.py" first!')
    sys.exit(1)

print('All Privilege Escalation Methods\n')
with open('privesc_methods.txt', 'w+') as f:
    for resource_type in permissions:  # Org, Folder, Proj, SA
        for resource in permissions[resource_type]:  # IDs of Orgs, Folders, Projs, SAs
            for member in permissions[resource_type][resource]:  # Members with permissions on the current resource
                check_privesc(permissions[resource_type][resource][member], resource_type, resource, member, f)

print('Misc. setIamPolicy Permissions\n')
with open('setIamPolicy_methods.txt', 'w+') as f:
    first_method = True
    for resource_type in permissions:  # Org, Folder, Proj, SA
        for resource in permissions[resource_type]:  # IDs of Orgs, Folders, Projs, SAs
            for member in permissions[resource_type][resource]:  # Members with permissions on the current resource
                for permission in permissions[resource_type][resource][member]:
                    if 'setIamPolicy' in permission:
                        if first_method:  # Only print out a user if there is a method associated with it
                            print(f'{member} on {resource_type[:-1]} {resource}:')
                            f.write(f'{member} on {resource_type[:-1]} {resource}:\n')
                            first_method = False
                        print(f'    {permission}')
                        f.write(f'    {permission}\n')
    if first_method is False:
        f.write('\n')

print('\nDone!')
print('Results output to ./privesc_methods.txt and ./setIamPolicy_methods.txt...')
