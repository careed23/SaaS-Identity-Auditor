def enforce_mfa_policy(audit_results):
    """
    If a user is an Admin and has no MFA, deactivate their access.
    """
    for result in audit_results:
        if result['role'] == 'admin' and not result['mfa_enabled']:
            print(f"⚠️ SECURITY VIOLATION: Deactivating {result['user']} - Missing MFA on Admin account.")
            # In a real scenario, you'd call the API to disable the account here:
            # identity_provider.deactivate_user(result['user'])
