import boto3
import requests
import json
import time
from datetime import datetime, timezone

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
threshold=80.0

secret_name='Telegram_bot_secrets'
secrets_client = boto3.client("secretsmanager", region_name=region)
secret_response = secrets_client.get_secret_value(SecretId=secret_name)
secret_dict = json.loads(secret_response["SecretString"])

TELEGRAM_BOT_TOKEN = secret_dict["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = secret_dict["TELEGRAM_CHAT_ID"]

def send_telegram_alert(instance_id, mem_usage):
    message= (f"🚨High Memory usage🚨 \n Instance: {instance_id}\n Region '{region}'\n Memory used: {mem_usage:.2f}%⚠️\n Timestamp: '{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}'")
    url= f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)
    


def get_memory_usage():
    ssm=boto3.client('ssm', region_name=region)
    response = ssm.describe_instance_information()
    commands = ["awk '/MemTotal/ {t=$2} /MemAvailable/ {a=$2} END {print 100-((a/t)*100)}' /proc/meminfo"]

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
            print(f"{BLUE}Checking memory usage{RESET}")
            time.sleep(3)
            output=ssm.get_command_invocation(CommandId=command_id,InstanceId=instance)
            print()
            result = output['StandardOutputContent'].strip()
            if not result:
                print("No memory data returned!")
            else:
                mem_used = float(result)
                print("Memory used is:",mem_used)
                if mem_used > threshold:
                    print(f"⚠️{RED}High memory usage detected for instance:{RESET} {instance}⚠️")
                    send_telegram_alert(instance, mem_used) 
                    print(f"📨 {BLUE}Alerts sent to telegram{RESET} 📨")
    print("Done")
    
try:
    get_memory_usage()
except Exception as e:
    print(f"Something went wrong: {e}")    
