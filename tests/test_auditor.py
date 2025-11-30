import unittest
import pandas as pd
from auditor import IdentityAuditor

class TestIdentityAuditor(unittest.TestCase):

    def setUp(self):
        """
        Setup run before every test.
        We create a dummy auditor and inject a mock DataFrame directly 
        so we don't need to read from disk.
        """
        # We use a dummy file path because we override self.df immediately
        self.auditor = IdentityAuditor(data_source="dummy.json", config_path="config.yaml")
        
        # Mock Data: 1 Stale User, 1 Shadow Admin, 1 Safe User
        data = [
            {"user_id": "1", "email": "stale@test.com", "role": "member", "mfa_enabled": True, "last_login_days_ago": 91, "department": "HR"},
            {"user_id": "2", "email": "admin@test.com", "role": "admin", "mfa_enabled": False, "last_login_days_ago": 5, "department": "IT"},
            {"user_id": "3", "email": "safe@test.com", "role": "member", "mfa_enabled": True, "last_login_days_ago": 10, "department": "Sales"}
        ]
        self.auditor.df = pd.DataFrame(data)

    def test_stale_account_detection(self):
        """Test if users > 90 days inactive are flagged."""
        # Run the audit logic
        self.auditor.run_audit()
        
        # Check specific user rows
        stale_user = self.auditor.df[self.auditor.df['email'] == 'stale@test.com'].iloc[0]
        safe_user = self.auditor.df[self.auditor.df['email'] == 'safe@test.com'].iloc[0]
        
        self.assertTrue(stale_user['violation_stale'], "User inactive for 91 days should be flagged as stale")
        self.assertFalse(safe_user['violation_stale'], "Active user should not be flagged")

    def test_shadow_admin_detection(self):
        """Test if Admins without MFA are flagged."""
        self.auditor.run_audit()
        
        shadow_admin = self.auditor.df[self.auditor.df['email'] == 'admin@test.com'].iloc[0]
        self.assertTrue(shadow_admin['violation_shadow_admin'], "Admin without MFA should be flagged")

    def test_risk_scoring(self):
        """Test if risk scores are calculated correctly."""
        self.auditor.run_audit()
        
        # Shadow admin (weight 2) + Not Stale (0) = 2
        shadow_admin = self.auditor.df[self.auditor.df['email'] == 'admin@test.com'].iloc[0]
        self.assertEqual(shadow_admin['risk_score'], 2)

if __name__ == '__main__':
    unittest.main()