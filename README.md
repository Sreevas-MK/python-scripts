# AWS Automation Scripts

A collection of practical **AWS DevOps automation scripts** written in Python.  
These scripts use **boto3** and **SSM RunCommand** to automate, monitor, and manage AWS infrastructure efficiently.

---

##  Repository Structure

├── ec2/ → EC2 operations (snapshots, reports, tagging, auto-stop)

├── monitoring/ → Monitoring & alerting scripts (CloudWatch, Telegram, SSM memory)

├── ssm/ → SSM RunCommand utilities for EC2 management

├── monitoring/ → Monitoring & alerting scripts (CloudWatch, Telegram, SSM memory)

├── ssm/ → SSM RunCommand utilities for EC2 management

├── README.md 

└── requirements.txt → Python dependencies


---

##  Setup

### Prerequisites
- Python 3.8 or higher  
- AWS CLI configured (`aws configure`)  
- IAM permissions for EC2, SSM, and CloudWatch  

### Installation

Users need Python and pip already installed and available in their environment.

#### Install Python (version 3.8 or higher)

On Ubuntu:
```bash
sudo apt install python3 python3-pip -y
```
On Amazon Linux 2 (yum):
```bash
sudo yum install python3 -y
```
Verify installation:
```bash
python3 --version
pip3 --version
```
Install git and clone the repository

```bash
sudo yum install git -y
git clone https://github.com/Sreevas-MK/python-scripts.git
cd python-scripts
```

Install all required Python libraries using:
```bash
pip install -r requirements.txt
```
---
### Tools & Libraries Used

- Python 3

- boto3 — AWS SDK for Python

- requests — For sending Telegram notifications

- AWS CLI — For credential configuration

---

## Script Categories

#### 1. EC2: Scripts for managing EC2 lifecycle and resources:

- autostop_nonprod_instances.py — Stops non-production instances automatically.

- snapshot_automation.py — Automates EBS snapshot creation and cleanup.

- system_report.py — Generates EC2 system reports.

- tag_automation.py — Adds or modifies instance tags dynamically.

#### 2. Monitoring: Scripts for monitoring and sending alerts:

- telegram_cloudwatch_cpu_alert.py — Sends CPU alerts to Telegram.

- ssm_memory_check_telegram.py — Checks EC2 memory usage via SSM and alerts via Telegram.

- ping_sweeper.py — Pings multiple hosts to verify reachability.

#### SSM: Scripts for remote execution using AWS Systems Manager:

- ssm_exec.py — Runs shell commands on EC2 instances via SSM RunCommand.

- ssm_exec_withpath.py — Executes commands from specific file paths on instances.

---
## Usage

Each script can be run directly from your EC2 instance:
```bash
python3 <script_name>.py
```
Example:
```bash
python3 monitoring/ssm_memory_check_telegram.py
```

Note: All scripts automatically use the IAM role credentials assigned to the EC2 instance.
Here’s the complete IAM policy you can attach to your EC2 IAM role:

```bash
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
---
## Conclusion

This repository provides a collection of Python-based AWS automation scripts designed to simplify everyday DevOps operations.

---
