# **S3 Inventory Reporting — AWS Python Scripts**

This folder contains a script to **scan S3 buckets**, count objects, calculate storage usage, and generate a readable **bucket inventory report**.

The script is useful for **cost audits, storage analysis, and bucket usage visibility**.

## Script Included

## S3 Bucket Inventory Report

**File:** `s3_inventory_report.py`

### Purpose

Scans all S3 buckets in a specified region and reports:

* Number of objects per bucket
* Total storage usage
* Object names
* Object size
* Last modified timestamps

##  What the Script Does

### Bucket-Level Actions:

* Lists all S3 buckets
* Scans buckets in the configured AWS region
* Skips empty buckets

### Object-Level Actions:

* Counts total objects
* Calculates total bucket size
* Prints each object's:

  * Key name
  * Size (MB)
  * Last modified time

## Example Output

```
Scanning bucket: my-app-backups

Total objects: 134

1. backups/db.sql - Size(MB): 52.4 - Last Modified: 2024-12-20
2. logs/app.log - Size(MB): 5.2 - Last Modified: 2024-12-18

REPORT COMPLETED
```

##  Configuration

Set AWS region in the script:

```python
region = "ap-south-1"
```

## How To Run

```bash
python3 s3_inventory_report.py
```

## IAM Permissions Required

Attach these permissions to your IAM Role:

```json
{
  "Effect": "Allow",
  "Action": [
    "s3:ListAllMyBuckets",
    "s3:ListBucket",
    "s3:GetObject"
  ],
  "Resource": "*"
}
```


## Performance & Cost Warning

This script:

* Lists **every object** in buckets
* Can take **long time** on large buckets
* Can generate **API request costs**

### Not recommended for:

* Buckets with **millions of objects**
* Production runs without filtering

---
