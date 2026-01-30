import boto3
from datetime import datetime, timezone


class AWSAuditor:
    def __init__(self):
        self.client = boto3.client('iam')

    def get_user_audit_data(self):
        users = self.client.list_users()['Users']
        audit_ready_data = []

        for user in users:
            # Check for MFA
            mfa = self.client.list_mfa_devices(UserName=user['UserName'])['MFADevices']

            # Check for Stale Keys (Last used > 90 days)
            access_keys = self.client.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
            stale_key = False
            for key in access_keys:
                last_used = self.client.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])
                usage_date = last_used.get('AccessKeyLastUsed', {}).get('LastUsedDate')
                if usage_date:
                    days_old = (datetime.now(timezone.utc) - usage_date).days
                    if days_old > 90:
                        stale_key = True

            audit_ready_data.append({
                "user": user['UserName'],
                "mfa_enabled": len(mfa) > 0,
                "stale_access_keys": stale_key,
                "last_login": user.get('PasswordLastUsed', 'Never')
            })
        return audit_ready_data
