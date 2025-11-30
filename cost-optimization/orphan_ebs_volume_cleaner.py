"""
===========================================================
EBS Orphan Volume Cleaner (Unattached Volume Cleanup Script)
===========================================================
This script scans AWS account for all EBS volumes( In the region defined) that are in 'available' state (not attached to any EC2 instance) and optionally deletes them to save cost.
===========================================================
"""

import boto3
import time

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

region = "ap-south-1"

def find_unattached_volumes():
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_volumes(Filters=[{'Name':'status','Values':['available']}])

        orphan_volumes = response.get('Volumes',[])
        print(f"{GREEN}Scanning unattached volumes at {region}....{RESET}")
        time.sleep(2)
        
        if not orphan_volumes:
            print(f"{BLUE}No unattached EBS volumes found at '{region}'.{RESET}")
            return

        print(f"{RED}Found unattached EBS volumes{RESET}")
        for volume in orphan_volumes:
            print(f"{MAGENTA}Volume ID:{RESET} {volume['VolumeId']}, {YELLOW}size:{RESET} {volume['Size']}GiB, {CYAN}AZ:{RESET} {volume['AvailabilityZone']}")

        delete = input(f"{RED}Do you want to delete all volumes? (yes/no):{RESET}").strip().lower()
        if delete == 'yes':
            for volume in orphan_volumes:
                volume_id = volume['VolumeId']
                ec2.delete_volume(VolumeId=volume_id)
                print(f"{GREEN}Deleted the volume: {volume_id}!{RESET}")

        else:
            print(f"{BLUE}No volumes were deleted{RESET}")
            
    except Exception as e:
        print(f"{RED}An error occurred:{e}{RESET}")

find_unattached_volumes()      
