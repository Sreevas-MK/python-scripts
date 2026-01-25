# **Cost Optimization — AWS Automation Scripts**

This directory contains **AWS cost optimization automation scripts** designed to identify and clean up unused or wasteful cloud resources.

The goal is to **reduce AWS spend safely** while keeping production resources protected.

## Scripts Overview

### 1. Auto Stop Non-Production EC2 Instances

**File:** `autostop_nonprod_instances.py`

**Purpose:**
Stops EC2 instances running **longer than 24 hours**, **excluding production instances**.

**Logic:**

* Scans running EC2 instances
* Skips instances tagged `Environment=Production`
* Stops instances older than 24 hours

**Use Case:**
Prevent wasted compute cost in dev/test environments.


### 2. Elastic IP (EIP) Auditor

**File:** `eip_auditor.py`

**Purpose:**
Finds **unused Elastic IPs** that generate unnecessary charges.

**Detects:**

* Unattached EIPs (cost-incurring)
* EIPs attached to EC2 or ENIs

**Use Case:**
Identify EIPs safe to release and save money.


### 3. Orphan EBS Volume Cleaner

**File:** `orphan_ebs_volume_cleaner.py`

**Purpose:**
Finds **unattached EBS volumes** and optionally deletes them.

**Logic:**

* Scans EBS volumes in `available` state
* Displays size and availability zone
* Prompts before deleting

**Use Case:**
Remove unused storage and reduce monthly EBS cost.


### 4️⃣ S3 Lifecycle Cleanup Script

**File:** `s3_lifecycle_manager.py`

**Purpose:**
Deletes **old S3 objects** based on age while protecting important buckets.

**Features:**

* Skips buckets with keywords like `logs`, `backup`
* Skips specific prefixes (`logs/`, `backup/`)
* Deletes objects older than configured days
* Ignores empty buckets

**Use Case:**
Reduce S3 storage costs without breaking backups or logs.


##  How To Run Scripts

```bash
python3 script_name.py
```

Examples:

```bash
python3 autostop_nonprod_instances.py
python3 eip_auditor.py
python3 orphan_ebs_volume_cleaner.py
python3 s3_lifecycle_manager.py
```

##  Notes

* Some scripts **delete resources** — review output before confirming
* Production EC2 instances are **explicitly protected**
* Always test in **non-production accounts first**

---
