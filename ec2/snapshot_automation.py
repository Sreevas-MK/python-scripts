""" AWS EC2 EBS Snapshot Automation Script
Creates snapshots for production instances and deletes old ones based on retention policy"""


import boto3, time
from datetime import datetime, timedelta, timezone

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

region="ap-south-1"

RETENTION_HOURS = 24
TAG_KEY = "CreatedBy"
TAG_VALUE = "AutoSnapshot"

try:
    ec2=boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(Filters=[{"Name":"instance-state-name","Values":["running"]}])

    print(f"🔍{BLUE}Scanning for running instances in{BLUE} {region}⌛\n")
    time.sleep(2)

    volumes_for_snapshot={}
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            tags=instance.get('Tags', [])
            
            tag_dict={}
            for tag in tags:
                key = tag['Key']
                value = tag['Value']
                tag_dict[key]=value

            if tag_dict.get("Environment", "").lower() == "production":
                instance_id=instance['InstanceId']
                print(f"🟡 {instance_id}{GREEN} is a Production instance.{RESET}")
                for vol in instance['BlockDeviceMappings']:
                    volume_id=vol['Ebs']['VolumeId']
                    if instance_id not in volumes_for_snapshot:
                        volumes_for_snapshot[instance_id] = []
                    volumes_for_snapshot[instance_id].append(volume_id)
            else:
                print(f"⚪ Skipping: {instance['InstanceId']} {BLUE}is not a production instance.{RESET}")

    print()
    if not volumes_for_snapshot:
        print(f"{CYAN}No production instances found. Skipping snapshot creation.{RESET}")
    else:
        for instance_id,volumes in volumes_for_snapshot.items():
            for volume_id in volumes:
                SNAP_NAME = datetime.now(timezone.utc).strftime(f"snapshot-%d-%b-%Y-time-%H.%M.%S-{volume_id}")
                snapshot_description=f"Automated snapshot for {instance_id}"
                snapshot=ec2.create_snapshot(VolumeId=volume_id, Description=snapshot_description, TagSpecifications=[{'ResourceType': 'snapshot','Tags':[{'Key': 'Name', 'Value': SNAP_NAME},{'Key': TAG_KEY, 'Value': TAG_VALUE},{'Key': 'InstanceId', 'Value': instance_id},{'Key': 'VolumeId', 'Value': volume_id}]}])
                print(f"{GREEN}Snapshot created for{RESET} {instance_id} : {volume_id}")

    time.sleep(3)

    print()
    delete_time=datetime.now(timezone.utc) - timedelta(hours=RETENTION_HOURS)
    response=ec2.describe_snapshots(Filters=[{"Name":f"tag:{TAG_KEY}","Values":[TAG_VALUE]},{"Name": "status", "Values": ["completed"]}])
    snapshots=response['Snapshots']
    print(f"🔍{BLUE}Scanning for old snapshots{RESET}⌛\n")

    if not snapshots:
        print("No snapshots found!")
    else:
        for snapshot in snapshots:
            if snapshot['StartTime'] < delete_time:
                print(f"{RED}Deleting the old snapshot:{RESET} {snapshot['SnapshotId']}")
                ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            else:
                print(f"{snapshot['SnapshotId']} {BLUE}was created within {RETENTION_HOURS} hours. Skipping!{RESET}")
        print()
    print(f"{GREEN}Completed{RESET}✅")

except Exception as e:
    print(f"{RED}Something went wrong:{RESET} {e}")
