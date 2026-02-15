import boto3
import json

region = "ap-south-1"

def lambda_handler(event, context):
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_addresses()
        addresses = response.get('Addresses', [])

        if not addresses:
            print(f"There are no Elastic IP's in this region.")
            
        unattached_eip = []
        attached_eip = []
        
        for address in addresses:
            public_ip = address.get("PublicIp")
            instance_id = address.get("InstanceId")
            network_interface_id = address.get("NetworkInterfaceId")
            
            if instance_id is None and network_interface_id is None:
                unattached_eip.append({"public_ip": public_ip, "instance_id": instance_id})
            elif instance_id or network_interface_id:
                attached_eip.append({"public_ip": public_ip, "instance_id": instance_id, "network_interface_id": network_interface_id})

        if unattached_eip:
            unattached_count = 1
            print(f"Unattached EIP's found!")
            for eip in unattached_eip:
                print(f"{unattached_count}. Public IP: {eip['public_ip']}")
                unattached_count += 1
    
        else:
            attached_count = 1
            for eip in attached_eip:
                if eip["instance_id"]:
                    print(f"{attached_count}. No unattached Elastic IPs! EIP {eip['public_ip']} is in use at Instance ID: {eip['instance_id']}.")
                elif eip["network_interface_id"]:
                    print(f"{attached_count}. No unattached Elastic IPs! EIP {eip['public_ip']} is in use at Network Interface ID: {eip['network_interface_id']}.")
                attached_count += 1

        return {
            'statusCode': 200,
            'body': json.dumps('Audit completed successfully')
        }

    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
