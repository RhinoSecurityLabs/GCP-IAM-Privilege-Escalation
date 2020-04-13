# IAM Privilege Escalation in GCP

## Table of Contents
- The `ExploitScripts` Folder
    - Contains exploit scripts for each of the privilege escalation methods outlined in the blog post, as well as a Cloud Function and Docker image for some of the methods that require them.
- The `PrivEscScanner` Folder
    - Containers a permissions enumerator for all members in a GCP account and an associated privilege escalation scanner that reviews the permissions in search of privilege escalation vulnerabilities.

For more information on these privilege escalation methods, how to exploit them, the permissions they require, and more, see the blog post on our website: BLOGLINK