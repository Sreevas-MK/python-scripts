"""
AWS EC2 Multi-Instance Ping Health Checker
Author: Sreevas M K
Description: Lists all running EC2 instances in a given AWS region
and performs a ping test on their public IPs.
"""

import boto3, subprocess

region=input("Enter a region:")

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


try:
    ec2=boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(Filters=[{"Name":"instance-state-name","Values":["running"]}])

    print(f"Ping results for running instances in region:{MAGENTA} {region} {RESET}")
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
            tags=instance['Tags']
            if not tags:
                name_tag = "-"
            else:
                for tag in tags:
                    name_tag =tag['Value']
            instance_details.append((instance_id, ip, name_tag ))
                    
    healthy=[]
    unhealthy=[]
    partially_healthy=[]

    if not instance_details:
        print("There are no running instances")

    else:
        count=1
        for instance_id,ip,name_tag in instance_details:
            ping = subprocess.getoutput(f"ping -c 3 {ip}")
            print(f"{count}. {instance_id}")
            print(f"{BLUE}{ping}{RESET}")

            if "0% packet loss" in ping:
                print(f"🟢 Instance is healthy 🟢")
                healthy.append((instance_id, name_tag))
            elif "100% packet loss" in ping:
                print(f"🔴 Instance is Unhealthy 🔴")
                unhealthy.append((instance_id,name_tag))
            else:
                print(f"🟡 Instance is partially healthy 🟡")
                partially_healthy.append((instance_id,name_tag))
                
            count+=1
            print()


    if not healthy:
        print(f"{RED}There are no healthy instances{RESET}")
    else:
        print(f"{GREEN}Healthy instances:{RESET}")
        for instance_id,name_tag in healthy:
            print(f"{instance_id} - {name_tag}")

    if not unhealthy:
        print(f"\n{RED}There are no unhealthy instances{RESET}")
    else:
        print(f"{RED}Unhealthy instances:{RESET}")
        for instance_id,name_tag in unhealthy:
            print(f"{instance_id} - {name_tag}")

    if not partially_healthy:
        print(f"\n{YELLOW}There are no partially healthy instances{RESET}")
    else:
        print(f"{YELLOW}Partially healthy instances:{RESET}")
        for instance_id,name_tag in partially_healthy:
            print(f"{instance_id} - {name_tag}")    

except Exception as e:
    print(f"{RED}Something went wrong:{RESET} {e}")
