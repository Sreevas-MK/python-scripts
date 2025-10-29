# SSM Command Execution (without SSH)

import boto3, time

region=input("Enter a region:")
commands=["df -h", "df -i", "uptime"]   


try:
    ssm=boto3.client('ssm', region_name=region)
    response = ssm.describe_instance_information()

    print()
    instances=[]
    for info in response['InstanceInformationList']:
        instance_id=info['InstanceId']

        if not instance_id:
            print("No instances found")
        else:
            print("Found instances")
            instances.append(instance_id)

    for instance in instances:
        print(f"Commands sent to {instance}")

        for cmd in commands:
            command_response=ssm.send_command(InstanceIds=[instance],DocumentName='AWS-RunShellScript',Parameters={"commands":[cmd]})
                
            command_id=command_response['Command']['CommandId']   
            print(f"Waiting for command execution: {cmd}")
            time.sleep(3)
            output=ssm.get_command_invocation(CommandId=command_id,InstanceId=instance)
            print()
            print(output['StandardOutputContent'].strip())
            print("-" * 60)
    print("Done")
    
except Exception as e:
    print(e)
