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

region = 'ap-south-1'
ec2=boto3.client('ec2', region_name=region)

def list_instances():
    instances=[]
    response = ec2.get_paginator('describe_instances')
    for page in response.paginate():
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                for tag in instance.get('Tags',[]):
                    if tag['Key']=='Name':
                        name=tag['Value']
                        break
                Instance_id=instance['InstanceId']
                State=instance['State']['Name']

                profile_associations=ec2.describe_iam_instance_profile_associations(Filters=[{'Name': 'instance-id', 'Values': [Instance_id]}])
                associations = profile_associations['IamInstanceProfileAssociations']
                if associations:
                    has_role=True
                    role_arn=associations[0]['IamInstanceProfile']['Arn']
                else:
                    has_role = False
                    role_arn=None

                instances.append({'Instance_id':Instance_id, 'State':State, 'Name':name, 'has_role':has_role, 'role_arn':role_arn})
    return instances


def role_compliance():
    instances_info=list_instances()

    compliant_instances=[]
    non_compliant_instances=[]
    compliant=0
    non_compliant=0

    for instance_details in instances_info:
        if instance_details['has_role']:
            compliant_instances.append(instance_details)
            compliant+=1
        else:
            non_compliant_instances.append(instance_details)
            non_compliant+=1

    print(f"{BOLD}{BLUE}Instances with IAM role:{RESET} {compliant}")
    running_count=1
    stopped_count=1
    print(f"\n{GREEN}Running instances:{RESET}")
    for instance in compliant_instances:
        if instance['State']=='running':
            print(f"{running_count}. Name: {instance['Name']}, Instance ID: {instance['Instance_id']}, Role: {RED}{instance['role_arn'].split('/')[-1]}{RESET}")
            running_count+=1
    if running_count ==1:
        print("There are no running instances")
            
    print(f"\n{MAGENTA}Stopped instances:{RESET}")
    for instance in compliant_instances:
        if instance['State']=='stopped':
            print(f"{stopped_count}. Name: {instance['Name']}, Instance ID: {instance['Instance_id']}, Role: {RED}{instance['role_arn'].split('/')[-1]}{RESET}")
            stopped_count+=1
    if stopped_count ==1:
        print("There are no stopped instances")

    print(f"\n--------------------------------------\n")

    print(f"{BOLD}{BLUE}Instances without IAM role:{RESET} {non_compliant}")
    running_count=1
    stopped_count=1
    print(f"\n{GREEN}Running instances:{RESET}")
    for instance in non_compliant_instances:
        if instance['State']=='running':
            print(f"{running_count}. Name: {instance['Name']}, Instance ID: {instance['Instance_id']}")
            running_count+=1
    if running_count ==1:
        print("There are no running instances")
            
    print(f"\n{MAGENTA}Stopped instances:{RESET}")
    for instance in non_compliant_instances:
        if instance['State']=='stopped':
            print(f"{stopped_count}. Name: {instance['Name']}, Instance ID: {instance['Instance_id']}")
            stopped_count+=1
    if stopped_count ==1:
        print("There are no stopped instances") 
role_compliance()
