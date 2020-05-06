# The GCP Privilege Escalation Scanner
Use these scripts to scan your project hierarchy for all permissions granted to all members, then check for privilege escalation vulnerabilities.

## Usage

1. Enumerate permissions in the project
    - `python3 enumerate_member_permissions.py --project-id test-project-12345`
2. Scan the enumerated permissions for privilege escalation vulnerabilities
    - `python3 check_for_privesc.py`
3. Review the results
    - `all_org_folder_proj_sa_permissions.json` – All members and their associated privileges
    - `privesc_methods.txt` – All detected privilege escalation methods
    - `setIamPolicy_methods.txt` – All detected setIamPolicy methods

## References

1. https://rhinosecuritylabs.com/cloud-security/privilege-escalation-google-cloud-platform-part-1/
2. https://rhinosecuritylabs.com/cloud-security/privilege-escalation-google-cloud-platform-part-2/