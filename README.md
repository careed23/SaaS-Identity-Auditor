<div align="center">

# 🛡️ SaaS Identity Auditor & Compliance Engine

**A containerized, config-driven security tool for enforcing Identity & Access Management (IAM) policies.**

![CI/CD Pipeline](https://img.shields.io/badge/Pipeline-Passing-green?style=for-the-badge&logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Container-Ready-blue?style=for-the-badge&logo=docker&logoColor=white)
![Security](https://img.shields.io/badge/Security-Bandit%20Scanned-secure?style=for-the-badge&logo=security&logoColor=white)

</div>

---

<div align="center">

## 📌 Project Overview

As organizations scale, "SaaS Sprawl" creates visibility gaps in identity management. The **SaaS Identity Auditor** is an automated engine designed to ingest user data, apply rigorous security policies (e.g., MFA mandates, Stale Account detection), and generate executive-level risk dashboards.

Designed with **DevSecOps principles**, this tool is fully containerized and includes a CI/CD pipeline that enforces code quality (Flake8), security scanning (Bandit), and logic verification (PyTest) on every commit.

</div>

---

<div align="center">

## 🚀 Key Features

**Zero Trust Enforcement**
Detects "Shadow Admins" (Privileged users without MFA).

**Attack Surface Reduction**
Automatically flags accounts inactive for 90+ days (Configurable).

**Config-as-Code**
All security thresholds and weighting logic are decoupled from code via `config.yaml`.

**Automated Visualization**
Generates a C-level executive dashboard (`.png`) and granular audit artifacts (`.csv`).

**Containerized**
Zero-dependency execution via Docker.

**Self-Healing**
Includes pre-built hooks for Slack/Teams alerting (simulated).

</div>

---

<div align="center">

## 🛠 Tech Stack

**Core:** Python 3.9, Pandas, NumPy
**Visualization:** Matplotlib
**Infrastructure:** Docker, GitHub Actions
**Quality & Security:** PyTest, Flake8, Bandit (SAST)

</div>

---

<div align="center">

## ⚙️ Configuration

Security policies are defined in `config.yaml` to allow for operational flexibility without code changes:

```yaml
policies:
  stale_account_threshold_days: 90
  mfa_required_roles:
    - "admin"
    - "super_admin"
