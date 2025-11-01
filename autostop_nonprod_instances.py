""" AWS EC2 - Auto-Stop Idle Instances
Description: Automated EC2 Instance Cleanup: Stop Non-Production Instances Running Over 24 Hours"""


import boto3, time
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

region=input(f"{BLUE}Enter a region:{RESET}").lower()
print()

try:
    ec2=boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(Filters=[{"Name":"instance-state-name","Values":["running"]}])

    print(f"🔍Scanning for running instances in {region}⌛")
    time.sleep(2)
    print()

    time_now=datetime.now(timezone.utc)
    threshold_time = time_now - timedelta(hours=24)

    instances_to_stop=[]
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id=instance['InstanceId']
            launch_time=instance["LaunchTime"]

            tags=instance.get('Tags', [])
            
            tag_dict={}
            for tag in tags:
                key = tag['Key']
                value = tag['Value']
                tag_dict[key]=value
                
            if tag_dict.get("Environment", "").lower() == "production":
                print(f"🟡 {instance_id} is a Production instance. Skipping.")
                continue

            if launch_time < threshold_time:
                print(f"🔴{instance_id}{RED} has been running for more than 24 hours.{RESET}")
                instances_to_stop.append(instance_id)
            else:
                print(f"🟢{instance_id} {GREEN}has been running for less than 24 hours.{RESET}")

    print()
    if not instances_to_stop:
         print(f"{BLUE}No instances need to be stopped. All are running for less than 24 hours.{RESET}")
    else:
        for instance_id in instances_to_stop:
            print(f"🛑Stopping instance {instance_id}....")
            ec2.stop_instances(InstanceIds=[instance_id])
            print(f"Instance stopped ✅")
           

except Exception as e:
    print(f"{RED}Something went wrong:{RESET} {e}")
