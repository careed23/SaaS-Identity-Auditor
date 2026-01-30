import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from remediate import enforce_mfa_policy


def test_enforce_mfa_policy_warns_admin(capsys):
    audit_results = [
        {"user": "alice", "role": "admin", "mfa_enabled": False},
        {"user": "bob", "role": "member", "mfa_enabled": False},
    ]

    enforce_mfa_policy(audit_results)
    captured = capsys.readouterr()

    assert "Deactivating alice" in captured.out
    assert "bob" not in captured.out
