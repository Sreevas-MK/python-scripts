# **EC2 Automation — AWS Python Scripts**

This folder contains **AWS EC2 automation scripts** to manage compute resources, enforce compliance, automate backups, generate reports, and standardize tagging.

All scripts use **boto3** and run using **IAM Role credentials** on an EC2 instance.

## Scripts Overview

## 1. EC2 IAM Role Compliance Report

**File:** `ec2_iam_role_report.py`

**Purpose:**
Identifies EC2 instances **with and without IAM roles**.

**What it does:**

* Lists all EC2 instances
* Detects IAM Instance Profile attachments
* Separates **compliant** vs **non-compliant** instances
* Categorizes by **running** and **stopped** state

**Use Case:**
Security & compliance auditing — ensure EC2 instances use IAM roles instead of access keys.

## 2. Automated EBS Snapshot Management

**File:** `snapshot_automation.py`

**Purpose:**
Creates **automated EBS snapshots** for **production instances** and deletes old snapshots.

**Logic:**

* Scans running EC2 instances
* Selects only instances tagged `Environment=Production`
* Creates snapshots for attached volumes
* Tags snapshots for tracking
* Deletes snapshots older than retention period

**Retention Policy:**

* Default: **24 hours**

**Use Case:**
Backup automation and storage cost control.

## 3. EC2 System Resource Report

**File:** `system_report.py`

**Purpose:**
Generates a **server health & resource usage report**.

**Reports:**

* Uptime & load average
* Memory usage
* Disk usage (highest usage highlighted)
* Inode usage

**Use Case:**
Quick health diagnostics for Linux EC2 instances.

## 4. EC2 Tag Automation

**File:** `tag_automation.py`

**Purpose:**
Automatically **adds standardized tags** to running EC2 instances missing tags.

**Default Tags Applied:**

* `Name`
* `Owner`
* `Environment`

**Logic:**

* Scans running EC2 instances
* Detects missing tags
* Applies predefined tags automatically

**Use Case:**
Tag governance, cost allocation, and environment organization.

##  How To Run Scripts

```bash
python3 script_name.py
```

### Examples:

```bash
python3 ec2_iam_role_report.py
python3 snapshot_automation.py
python3 system_report.py
python3 tag_automation.py
```

## Requirements

* Python 3.x
* AWS CLI configured
* IAM Role attached to instance
* Required permissions:

  * EC2
  * IAM Instance Profile
  * EBS Snapshots

##  Notes

* Snapshot script **creates and deletes AWS resources**
* Tag automation **modifies instance metadata**
* Always validate in **non-production first**

---
