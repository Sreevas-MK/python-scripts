"""
AWS EC2 Instance Tag Automation
Author: Sreevas M K
Description: Automatically tag all untagged running instances with something like: {"Name": "DevOps", "Environment": "Test"}. etc
"""

import boto3, time

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

region=input(f"{BLUE}Enter a region:{RESET}").lower()

TAGS_TO_ADD = [
    {"Key": "Name", "Value":"Python-Revision-Server"},
    {"Key": "Owner", "Value": "Sreevas"},
    {"Key": "Environment", "Value": "Dev"}
]


try:
    ec2=boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(Filters=[{"Name":"instance-state-name","Values":["running"]}])

    print(f"{GREEN}\n🕑Scanning tags for instances in region:{RESET}{MAGENTA} {region} {RESET}....")
    time.sleep(2)
    
    print()

    instance_details=[]

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id=instance['InstanceId']
            network = instance['NetworkInterfaces'][0]
            if 'Association' in network and 'PublicIp' in network['Association']:
                ip = instance['NetworkInterfaces'][0]['Association']['PublicIp']
            else:
                ip = instance['PrivateIpAddress']
            tags=instance.get('Tags', [])
            if not tags:
                ec2.create_tags(Resources=[instance_id], Tags=TAGS_TO_ADD )
                print(f"{GREEN}Tag added for instance {instance_id}{RESET}✅")
            else:
                print(f"{BLUE}🟢Instance{RESET} '{instance_id}' {BLUE}already have tags{RESET}.")

except Exception as e:
    print(f"{RED}Something went wrong:{RESET} {e}")
