# **AWS SSM Remote Command Execution — Python Scripts**

This folder contains scripts to **execute commands remotely on EC2 instances using AWS Systems Manager (SSM)** — without SSH, keys, or inbound ports.

These scripts are useful for **fleet management, diagnostics, automation, and secure remote operations**.

## Scripts Included

## 1. **SSM Execute Shell Commands on EC2**

**File:** `ssm_exec.py`

### Purpose

Runs **multiple shell commands** on all **SSM-managed EC2 instances** in a specified AWS region.

### Commands Executed by Default

```python
commands = ["df -h", "df -i", "uptime"]
```

### What It Does

* Detects all SSM-managed EC2 instances
* Sends commands using `AWS-RunShellScript`
* Waits for execution
* Fetches and prints command output per instance
* Works **without SSH access**


### Run the Script

```bash
python3 ssm_exec.py
```

You will be prompted to enter a region:

```
Enter a region: ap-south-1
```

### Example Output

```
Found instances
Commands sent to i-0123456789abcdef

df -h output...
------------------------------------------------------------
uptime output...
------------------------------------------------------------
Done
```
---

##  2. **SSM Execute Script File on EC2**

**File:** `ssm_exec_withpath.py`

### Purpose

Executes a **Python script stored on EC2 instances** using SSM.

### Default Script Path

```python
commands_path = "/home/ec2-user/scripts/system_report.py"
```

### What It Does

* Finds all SSM-managed EC2 instances
* Executes a **remote script** via SSM
* Captures output
* Displays results per instance
* Includes **color-coded terminal output**

### Run the Script

```bash
python3 ssm_exec_withpath.py
```

### 📤 Example Output

```
Instances found ☑️
Commands sent to: i-0abcd1234
Waiting for command execution...
System Report Output...
------------------------------------------------------------
Done ✅
```

## IAM Permissions Required

Attach this IAM policy to the EC2 IAM Role or user:

```json
{
  "Effect": "Allow",
  "Action": [
    "ssm:SendCommand",
    "ssm:GetCommandInvocation",
    "ssm:DescribeInstanceInformation",
    "ssm:ListCommands",
    "ssm:ListCommandInvocations"
  ],
  "Resource": "*"
}
```

## Prerequisites

* EC2 instances must:

  * Have **SSM Agent installed**
  * Be registered in **AWS Systems Manager**
  * Have an **IAM Role with SSM permissions**
* Python 3 installed
* AWS credentials configured (`aws configure`)

##  Why Use SSM Instead of SSH?

- No inbound SSH ports
- No key pair management
- Works behind private subnets
- Secure, auditable execution
- Scales to **hundreds of instances**

---
