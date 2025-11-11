"""==============================================================
 AWS SSM REMOTE COMMAND EXECUTION SCRIPT ( using commands/script path)
==============================================================
Author: Sreevas M K
Description:
    This script connects to AWS Systems Manager (SSM) and executes 
    remote shell commands on all managed EC2 instances within a 
    specified region."""

import boto3, time

region=input("Enter a region:")
commands_path="/home/ec2-user/scripts/system_report.py"

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

print(f"{CYAN}Looking up for instances at: {RESET}{region}")



try:
    ssm=boto3.client('ssm', region_name=region)
    response = ssm.describe_instance_information()

    print()
    instances=[]
    for info in response['InstanceInformationList']:
        instance_id=info['InstanceId']

        if not instance_id:
            print(f"{RED}No instances found‼️{RESET}")
        else:
            print(f"{GREEN}Instances found ☑️{RESET}")
            instances.append(instance_id)

    for instance in instances:
        print(f"{BLUE}Commands sent to{RESET}: {instance}")
        command_response=ssm.send_command(InstanceIds=[instance],DocumentName='AWS-RunShellScript',Parameters={"commands": [f"python3 {commands_path}"]})
                
        command_id=command_response['Command']['CommandId']   
        print(f"{YELLOW}Waiting for command execution....{RESET}🕐")
        time.sleep(5)
        output=ssm.get_command_invocation(CommandId=command_id,InstanceId=instance)
        print()
        print(output['StandardOutputContent'].strip())
        print("-" * 60)
    print("Done✅")
    
except Exception as e:
    print(e)
