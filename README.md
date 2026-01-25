# AWS Automation Scripts (Python + Boto3)

A collection of ** AWS DevOps automation scripts** written in Python.  
These scripts use **boto3** and **AWS Systems Manager (SSM RunCommand)** to automate infrastructure operations, monitoring, cost optimization, and reporting.

## Repository Structure

```

python-scripts/
├── cost-optimization/   → Cost saving & cleanup automation
├── ec2/                 → EC2 lifecycle & governance scripts
├── monitoring/          → Alerts, CloudWatch, Telegram integrations
├── s3/                  → S3 automation & reporting
├── ssm/                 → Remote execution via AWS SSM RunCommand
├── requirements.txt     → Python dependencies
└── README.md            → Main documentation

````

## Setup & Installation

### Prerequisites

- Python **3.8+**
- AWS CLI configured (`aws configure`)
- IAM Role with permissions for EC2, SSM, CloudWatch, S3, Secrets Manager

### Install Python

**Ubuntu**
```bash
sudo apt install python3 python3-pip -y
````

**Amazon Linux**

```bash
sudo yum install python3 -y
```

Verify:

```bash
python3 --version
pip3 --version
```

### Clone Repository

```bash
sudo yum install git -y
git clone https://github.com/Sreevas-MK/python-scripts.git
cd python-scripts
```

### Install Dependencies

```bash
pip install -r requirements.txt
```
---

## Script Categories & Use Cases

### 1. Cost Optimization

Scripts to reduce AWS spend and clean unused resources.

* `autostop_nonprod_instances.py` — Stops non-production EC2 instances
* `eip_auditor.py` — Finds unused Elastic IPs
* `orphan_ebs_volume_cleaner.py` — Deletes unattached EBS volumes
* `s3_lifecycle_manager.py` — Automates S3 lifecycle policies


### 2. EC2 Management

Lifecycle automation, tagging, auditing, and reporting.

* `snapshot_automation.py` — Automates EBS snapshots + cleanup
* `system_report.py` — Generates EC2 health/system reports
* `tag_automation.py` — Auto-assigns and updates tags
* `ec2_iam_role_report.py` — Reports IAM roles attached to EC2


### 3. Monitoring & Alerts

Operational monitoring + Telegram alerting.

* `telegram_cloudwatch_cpu_alert.py` — CPU alerts via Telegram
* `ssm_memory_check_telegram.py` — Memory usage alerts via SSM
* `cloudwatch_ebs_alerts.py` — EBS health alerts
* `ebs_iops_alerts.py` — Detects IOPS spikes
* `ping_sweeper.py` — Host reachability checks


### 4. S3 Automation

* `s3_inventory_report.py` — Generates S3 inventory reports


### 5. SSM Automation (Remote Execution)

* `ssm_exec.py` — Execute shell commands via SSM RunCommand
* `ssm_exec_withpath.py` — Execute commands from script files


## Usage

Run any script directly:

```bash
python3 path/to/script.py
```

Example:

```bash
python3 monitoring/ssm_memory_check_telegram.py
```

---

## IAM Role Policy (Attach to EC2 Instance Role)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StartInstances",
        "ec2:StopInstances",
        "ec2:CreateSnapshot",
        "ec2:DeleteSnapshot",
        "ec2:DescribeVolumes",
        "ec2:DescribeTags",
        "ec2:CreateTags",
        "ssm:SendCommand",
        "ssm:GetCommandInvocation",
        "ssm:DescribeInstanceInformation",
        "ssm:ListCommands",
        "ssm:ListCommandInvocations",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "secretsmanager:GetSecretValue",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

## Conclusion

This repository provides a collection of Python-based AWS automation scripts designed to simplify everyday DevOps operations.

---
