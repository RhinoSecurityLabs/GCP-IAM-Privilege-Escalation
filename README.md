# IAM Privilege Escalation in GCP

## Table of Contents
- The `ExploitScripts` Folder
    - Contains exploit scripts for each of the privilege escalation methods outlined in the blog post, as well as a Cloud Function and Docker image for some of the methods that require them.
- The `PrivEscScanner` Folder
    - Containers a permissions enumerator for all members in a GCP account and an associated privilege escalation scanner that reviews the permissions in search of privilege escalation vulnerabilities.

For more information on these privilege escalation methods, how to exploit them, the permissions they require, and more, see the blog post on our website: BLOGLINK

Current list of GCP IAM privilege escalation methods:

1. `cloudbuilds.builds.create`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/cloudbuild.builds.create.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/working-as-intendedrce-to-iam-privilege-escalation-in-gcp)  
2. `deploymentmanager.deployments.create`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/deploymentmanager.deployments.create.py) / [Blog Post]()
3. `iam.roles.update`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.roles.update.py) / [Blog Post]()
4. `iam.serviceAccounts.getAccessToken`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/ian.serviceAccounts.getAccessToken.py) / [Blog Post]()
5. `iam.serviceAccountKeys.create`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.serviceAccountKeys.create.py) / [Blog Post]()
6. `iam.serviceAccounts.implicitDelegation`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.serviceAccounts.implicitDelegation.py) / [Blog Post]()
7. `iam.serviceAccounts.signBlob`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.serviceAccounts.signBlob-accessToken.py) / [Blog Post]()
8. `iam.serviceAccounts.signJwt`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.serviceAccounts.signJwt.py) / [Blog Post]()
9. `cloudfunctions.functions.create`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/cloudfunctions.functions.create-call.py) / [Blog Post]()
10. `cloudfunctions.functions.update`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/cloudfunctions.functions.update.py) / [Blog Post]()
11. `compute.instances.create`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/compute.instances.create.py) / [Blog Post]()
12. `run.services.create`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/run.services.create.py) / [Blog Post]()
13. `cloudscheduler.jobs.create`: [Blog Post]()
14. `orgpolicy.policy.set`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/orgpolicy.policy.set.py) / [Blog Post]()
15. `storage.hmacKeys.create`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/storage.hmacKeys.create.py) / [Blog Post]()
16. `serviceusage.apiKeys.create`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/serviceusage.apiKeys.create.py) / [Blog Post]()
17. `serviceusage.apiKeys.list`: [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/serviceusage.apiKeys.list.py) / [Blog Post]()
