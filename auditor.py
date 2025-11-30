import pandas as pd
import json
import os
import yaml  # Requires PyYAML
from datetime import datetime
from typing import List, Dict, Any

# Default config fallback
DEFAULT_CONFIG = {
    "policies": {"stale_account_threshold_days": 90, "mfa_required_roles": ["admin"]},
    "compliance": {"risk_score_weights": {"stale_account": 1, "shadow_admin": 2}}
}

class IdentityAuditor:
    """
    A class to ingest SaaS user data and perform security compliance checks.
    Now supports Config-as-Code and Automated Alerting.
    """

    def __init__(self, data_source: str, config_path: str = "config.yaml"):
        self.data_source = data_source
        self.config = self._load_config(config_path)
        self.df = pd.DataFrame()

    def _load_config(self, path: str) -> Dict[str, Any]:
        """Loads policy configuration from YAML."""
        if not os.path.exists(path):
            print(f"[-] Config file {path} not found. Using defaults.")
            return DEFAULT_CONFIG
        
        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
                print(f"[+] Loaded security policies from {path}")
                return config
        except Exception as e:
            print(f"[-] Error loading config: {e}. Using defaults.")
            return DEFAULT_CONFIG

    def load_data(self) -> None:
        """Loads JSON data into a Pandas DataFrame for analysis."""
        try:
            with open(self.data_source, 'r') as f:
                data = json.load(f)
                self.df = pd.DataFrame(data)
                print(f"[+] Data loaded successfully: {len(self.df)} users found.")
        except FileNotFoundError:
            print(f"[-] Error: File {self.data_source} not found.")
        except Exception as e:
            print(f"[-] Error loading data: {e}")

    def run_audit(self) -> None:
        """Applies security logic based on loaded config."""
        if self.df.empty:
            print("[-] No data to audit.")
            return

        print("\n[+] Running Policy Checks...")
        
        # 1. Check for Stale Accounts (Dynamic Threshold)
        threshold = self.config['policies']['stale_account_threshold_days']
        self.df['violation_stale'] = self.df['last_login_days_ago'] > threshold

        # 2. Check for "Shadow Admins" (Dynamic Role List)
        privileged_roles = self.config['policies']['mfa_required_roles']
        
        self.df['violation_shadow_admin'] = (
            (self.df['role'].isin(privileged_roles)) & 
            (self.df['mfa_enabled'] == False)
        )

        # 3. Calculate Overall Risk Score (Dynamic Weights)
        weights = self.config['compliance']['risk_score_weights']
        
        self.df['risk_score'] = (
            self.df['violation_stale'].astype(int) * weights.get('stale_account', 1) + 
            self.df['violation_shadow_admin'].astype(int) * weights.get('shadow_admin', 2)
        )

        self._print_summary()
        self._trigger_alerts()

    def _trigger_alerts(self) -> None:
        """Simulates sending a Slack webhook for critical risks."""
        shadow_admins = self.df[self.df['violation_shadow_admin'] == True]
        
        if not shadow_admins.empty and self.config.get('alerting', {}).get('slack_webhook_enabled'):
            print("\n[!] CRITICAL ALERT: Triggering Slack Notification...")
            for _, user in shadow_admins.iterrows():
                # In a real app, this would be requests.post(webhook_url, json=payload)
                payload = {
                    "text": f":rotating_light: SECURITY ALERT: Shadow Admin Detected!",
                    "fields": [
                        {"title": "User", "value": user['email']},
                        {"title": "Role", "value": user['role']},
                        {"title": "Department", "value": user['department']}
                    ]
                }
                print(f"    >> Sending payload to {self.config['alerting']['slack_channel']}: {json.dumps(payload)}")

    def _print_summary(self) -> None:
        """Prints a high-level summary to the console."""
        total_users = len(self.df)
        stale_users = self.df['violation_stale'].sum()
        shadow_admins = self.df['violation_shadow_admin'].sum()

        print("-" * 40)
        print(f"AUDIT SUMMARY REPORT")
        print("-" * 40)
        print(f"Total Users Scanned: {total_users}")
        print(f"Stale Accounts Found: {stale_users}")
        print(f"Shadow Admins Found:  {shadow_admins} (CRITICAL)")
        print("-" * 40)

    def export_report(self) -> None:
        """Exports the audited data to a CSV file."""
        if self.df.empty:
            return
        
        filename = f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.df.to_csv(filename, index=False)
        print(f"[+] Full audit report generated: {filename}")

def main():
    # Path to the mock data file
    data_file = "mock_users.json"
    if not os.path.exists(data_file):
        if os.path.exists(os.path.join("data", data_file)):
            data_file = os.path.join("data", data_file)

    auditor = IdentityAuditor(data_file)
    auditor.load_data()
    auditor.run_audit()
    auditor.export_report()

if __name__ == "__main__":
    main()