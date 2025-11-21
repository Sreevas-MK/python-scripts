"""
Script Name: s3 Bucket Inventory Report
Purpose: Scan all S3 buckets in a given region, count objects, calculate size, and print a readable inventory report.
"""

import boto3

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

print(f"\n{BOLD}{MAGENTA}================= S3 Bucket Inventory Report Script ================={RESET}\n")

def scan_each_bucket():
    try:
        buckets = s3_client.list_buckets().get("Buckets", [])
    except Exception as e:
        print("Error listing buckets")
        return

    for bucket in buckets:
        bucket_name=bucket["Name"]
        
        print(f"{BOLD}{BLUE}🪣 Scanning bucket:{RESET} {bucket_name}\n")
        calculate_size(bucket_name)

def calculate_size(bucket_name):
    try:
        response = s3_client.get_paginator('list_objects_v2')
    except Exception as e:
        print(f"{RED}Error creating pagination for:{RESET} {bucket_name}: {RED}{e}{RESET}")
        return
        
    total_objects = 0
    total_size=0

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

        obj_count=1
        for obj in page['Contents']:
            total_objects+=1
            total_size+=obj['Size']
            print(f"{obj_count}. {obj['Key']}\t-Size(MB):, {round(obj['Size'] / (1024 * 1024), 2)}, Last Modified:, {obj['LastModified']}")
            obj_count+=1
    print()


scan_each_bucket()

print(f"\n{BOLD}{GREEN}================= REPORT COMPLETED ================={RESET}")        
