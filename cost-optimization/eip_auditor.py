"""
==========================================================================
Script Name: EIP auditor
Purpose    : Lists all Elastic IPs in the specified AWS region and
             identifies which ones are unattached (cost-incurring)
             and which ones are attached to instances or network interfaces.
==========================================================================
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

region = "ap-south-1"

def find_unattached_eip():
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_addresses()
        addresses = response.get('Addresses',[])

        if not addresses:
            print(f"{BLUE}There are no Elastic IP's in this region{RESET}.")
            
        unattached_eip = []
        attached_eip = []
        
        for address in addresses:
            public_ip = address.get("PublicIp")
            instance_id = address.get("InstanceId")
            network_interface_id = address.get("NetworkInterfaceId")
            
            # An Elastic IP can be attached either to an Instance OR to a Network Interface (ENI), not always directly to an Instance
            
            if instance_id is None and network_interface_id is None:
                unattached_eip.append({"public_ip":public_ip, "instance_id":instance_id})
            elif instance_id or network_interface_id:
                attached_eip.append({"public_ip":public_ip, "instance_id":instance_id, "network_interface_id": network_interface_id})

        if unattached_eip:
            unattached_count=1
            print(f"{RED}Unattached EIP's found!{RESET}")
            for eip in unattached_eip:
                print(f"{unattached_count}. Public IP: {eip['public_ip']}")
                unattached_count+=1
    
        else:
            attached_count=1
            for eip in attached_eip:
                if eip["instance_id"]:
                    print(f"{attached_count}. {GREEN}No unattached Elastic IPs!{RESET} EIP {RED}{eip['public_ip']}{RESET} is in use at Instance ID: {RED}{eip['instance_id']}{RESET}.")
                elif eip["network_interface_id"]:
                    print(f"{attached_count}. {GREEN}No unattached Elastic IPs!{RESET} EIP {RED}{eip['public_ip']}{RESET} is in use at Network Interface ID: {RED}{eip['network_interface_id']}{RESET}.")

                attached_count+=1

    except Exception as e:
        print(f"{RED}Error occurred:{RESET} {e}")                    

find_unattached_eip()
