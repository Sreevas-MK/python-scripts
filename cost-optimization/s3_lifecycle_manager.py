"""
S3 LIFECYCLE CLEANUP SCRIPT 

- This script scans all S3 buckets in the AWS region defined and deletes objects older than a given number of days.
- Skips entire buckets if their names contain keywords (example: "logs", "backup")
- Skips specific folder prefixes inside buckets (example: logs/, backup/)
- Ignores empty buckets
"""

import boto3
from datetime import datetime, timezone, timedelta

# Colors
RED = "\033[91m"       
GREEN = "\033[92m"   
YELLOW = "\033[93m"    
BLUE = "\033[94m"      
MAGENTA = "\033[95m"   
CYAN = "\033[96m"      
WHITE = "\033[97m"    
RESET = "\033[0m"     
BOLD = "\033[1m"

region='ap-south-1'
s3_client = boto3.client('s3', region_name=region)

SKIP_BUCKET_KEYWORDS = ["log", "logs", "backup"]
SKIP_PREFIXES = ['logs/','backup/']
DAYS_THRESHOLD = 0

print(f"\n{BOLD}{MAGENTA}================= S3 CLEANUP SCRIPT STARTED ================={RESET}\n")

def delete_objects_each_buckets():
    threshold_date = datetime.now(timezone.utc) - timedelta(days=DAYS_THRESHOLD)
    try:
        buckets = s3_client.list_buckets().get("Buckets", [])
    except Exception as e:
        print("Error listing buckets")
        return
    count=1

    for bucket in buckets:
        bucket_name=bucket["Name"]
        
        skip_bucket=False
        for key_word in SKIP_BUCKET_KEYWORDS:
            if key_word.lower() in bucket_name.lower():
                print(f"\n{count}. {BOLD}{BLUE}Skipping entire bucket:{RESET} {bucket_name}")
                print(f"\n{BLUE}Keyword found! -{RESET} '{key_word}'")
                skip_bucket=True
                break
        if skip_bucket:
            continue
            
        print(f"{count}. {BOLD}{BLUE}Scanning bucket:{RESET} {bucket_name}\n")
        count+=1
        
        delete_old_objects(bucket_name, threshold_date)


def delete_old_objects(bucket_name, threshold_date):
    try:
        response = s3_client.get_paginator('list_objects_v2')
    except Exception as e:
        print(f"{RED}Error creating pagination for:{RESET} {bucket_name}: {RED}{e}{RESET}")
        return
        
    total_objects = 0
    deleted_count=0
    retained_count=0

    for page in response.paginate(Bucket=bucket_name):
        if 'Contents' in page:
            total_objects+=len(page["Contents"])
    print(f"{CYAN}Total objects:{RESET} {total_objects}")

    if total_objects == 0:
        print(f"{YELLOW}Bucket is empty. Skipping the bucket.{RESET}\n")
        return

    for page in response.paginate(Bucket=bucket_name):
        if 'Contents' not in page:
            continue
            
        for obj in page['Contents']:
            key=obj['Key']
            last_modified=obj['LastModified']

            skip_this_object = False
            for prefix in SKIP_PREFIXES:
                if key.startswith(prefix):
                    skip_this_object = True
                    print(f"{GREEN}Skipping:{RESET} {key}, {GREEN}Last Modified:{RESET} {last_modified}")
                    retained_count+=1
                    break

            if skip_this_object:
                continue

            if last_modified < threshold_date:
                try:
                    s3_client.delete_object(Bucket=bucket_name, Key=key)
                    deleted_count+=1
                    print(f"{RED}Deleted:{RESET} {key}, {RED}Last Modified:{RESET} {last_modified}")
                except Exception as e:
                    print(f"{RED}Error deleting:{RESET} {key}")

    print(f"\n{MAGENTA}Total objects deleted:{RESET} {deleted_count}")
    print(f"{MAGENTA}Total objects retained:{RESET} {retained_count}\n")

delete_objects_each_buckets()

print(f"\n{BOLD}{GREEN}================= CLEANUP COMPLETED ================={RESET}")
