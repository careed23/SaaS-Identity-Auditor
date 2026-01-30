<div align="center">

# 🛡️ SaaS Identity Auditor & Compliance Engine 🛡️

**A containerized, config-driven security tool for enforcing Identity & Access Management (IAM) policies.**

![CI/CD Pipeline](https://img.shields.io/badge/Pipeline-Passing-green?style=for-the-badge&logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Container-Ready-blue?style=for-the-badge&logo=docker&logoColor=white)
![Security](https://img.shields.io/badge/Security-Bandit%20Scanned-secure?style=for-the-badge&logo=security&logoColor=white)

</div>

---

## 📌 Project Overview
As organizations scale, "SaaS Sprawl" creates visibility gaps in identity management. The **SaaS Identity Auditor** is an automated engine designed to ingest user data, apply rigorous security policies (e.g., MFA mandates, Stale Account detection), and generate executive-level risk dashboards. It is ideal for Cloud Architects, IAM teams, and MSPs standardizing identity governance at scale.

Designed with **DevSecOps principles**, this tool is fully containerized and includes a CI/CD pipeline that enforces code quality (Flake8), security scanning (Bandit), and logic verification (PyTest) on every commit.

## 🚀 Key Features
* **Zero Trust Enforcement:** Detects "Shadow Admins" (Privileged users without MFA).
* **Attack Surface Reduction:** Automatically flags accounts inactive for 90+ days (Configurable).
* **Config-as-Code:** All security thresholds and weighting logic are decoupled from code via `config.yaml`.
* **Automated Visualization:** Generates a C-level executive dashboard (`.png`) and granular audit artifacts (`.csv`).
* **Containerized:** Zero-dependency execution via Docker.
* **Self-Healing:** Includes pre-built hooks for Slack/Teams alerting (simulated).

## 🛠 Tech Stack
* **Core:** Python 3.9, Pandas, NumPy
* **Visualization:** Matplotlib
* **Infrastructure:** Docker, GitHub Actions
* **Quality & Security:** PyTest, Flake8, Bandit (SAST)

## 👷 Cloud Architect Use Cases
**Multi-Tenant SaaS Auditing**
* Audit identity posture across disconnected SaaS applications (Okta, Entra, Google Workspace, Slack).
* Enforce uniform security baselines (MFA mandates, account lifecycle policies) via config-as-code.

**Compliance & Audit Automation**
* Auto-generate executive dashboards for SOC2, ISO 27001, and HIPAA audit trails.
* Risk-scored CSV exports integrate with SIEM/GRC platforms (Splunk, Sentinel, ServiceNow).

**Zero Trust Implementation**
* Automated "Shadow Admin" detection prevents privilege escalation blind spots.
* Stale account quarantining reduces insider threat surface in hybrid environments.

**DevSecOps Governance**
* Decoupled policy management (`config.yaml`) enables security teams to enforce rules without code releases.
* CI/CD integration triggers automated remediation workflows.

## 🧭 Suggested Enhancements
* Add connectors to pull identities directly from SaaS APIs (Okta, Entra ID, Google Workspace) instead of JSON files.
* Map risk scores to cloud governance frameworks (CIS, NIST 800-53) for standardized reporting.
* Publish findings to SIEM/GRC tools via webhooks for continuous control monitoring.
* Support multi-tenant configuration bundles to enforce per-business-unit baselines.

## ⚙️ Configuration
Security policies are defined in `config.yaml` to allow for operational flexibility without code changes:

```yaml
policies:
  stale_account_threshold_days: 90
  mfa_required_roles:
    - "admin"
    - "super_admin"
