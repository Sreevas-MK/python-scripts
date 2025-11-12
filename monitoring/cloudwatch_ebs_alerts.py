import boto3
import requests
import json
import time
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

region = 'ap-south-1'

# Define thresholds for each metric
THRESHOLDS = {
    "VolumeReadOps": 150,       # read ops/sec
    "VolumeWriteOps": 150,      # write ops/sec
    "VolumeReadBytes": 3e6,      # 3 MB/sec
    "VolumeWriteBytes": 3e6,     # 3 MB/sec
    "VolumeQueueLength": 5,     # >5 requests queued
    "VolumeIdleTime": 20         # idle seconds (low value = busy)
}

secret_name='Telegram_bot_secrets'
secrets_client = boto3.client("secretsmanager", region_name=region)
secret_response = secrets_client.get_secret_value(SecretId=secret_name)
secret_dict = json.loads(secret_response["SecretString"])

TELEGRAM_BOT_TOKEN = secret_dict["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = secret_dict["TELEGRAM_CHAT_ID"]

def send_telegram_alert(volume_id, metric, usage, threshold):
    message= (f"🚨High I/O usage🚨 \n Volume: {volume_id}\n Region:'{region}'\n Metric: {metric}\n Threshold: {threshold}\n Usage: {usage} Timestamp: '{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}'")
    url= f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def get_volumes():
    volumes=[]
    ec2=boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(Filters=[{"Name":"instance-state-name","Values":["running"]}])
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for mapping in instance['BlockDeviceMappings']:
                volume_id = mapping['Ebs']['VolumeId']
                volumes.append(volume_id)
    return volumes

def get_metric(volume_id, metric_name):
    end_time = datetime.now(timezone.utc)
    start_time= end_time - timedelta(minutes=10)
    client = boto3.client('cloudwatch', region_name=region)
    metrics= client.get_metric_statistics(
        Namespace='AWS/EBS',
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'VolumeId',
                'Value': volume_id
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=[
            'Average',
        ]
    )
        
    datapoints = metrics["Datapoints"]
    if len(datapoints) > 0:
        # Sort datapoints by timestamp to ensure the latest comes last
        datapoints.sort(key=lambda x: x["Timestamp"])
        last_point=datapoints[-1]
        return last_point["Average"]
    else:
        return None

def check_ebs_usage():
    volumes=get_volumes()
    if not volumes:
        print(f"No running instances found")
        return
    count=1
    for volume in volumes:
        print(f"{count}. {BLUE}Usage for volume:{RESET} {volume}")
        alert_sent = False
        for metric, threshold in THRESHOLDS.items():
            usage=get_metric(volume,metric)
            if usage is None:
                print(f"{CYAN}No metrics for:{RESET} {volume}")
            else:
                print(f"{BLUE}Metric:{RESET}{metric} {BLUE}has usage:{RESET} {usage}, {BLUE}Threshold:{RESET} {threshold}")
                if metric == "VolumeIdleTime" and usage < threshold:
                    print(f"{RED}🚨 Low idle time detected! 🚨{RESET}")
                    send_telegram_alert(volume, metric, usage, threshold)
                    print(f"📨{MAGENTA}Alerts sent{RESET}📨" )
                    alert_sent=True
                    
                elif metric != "VolumeIdleTime" and usage > threshold:
                    print(f"{RED}🚨High usage detected for{RESET} {metric}🚨")
                    send_telegram_alert(volume, metric, usage, threshold)
                    print(f"📨{MAGENTA}Alerts sent{RESET}📨" )
                    alert_sent=True
        if not alert_sent:
            print(f"{GREEN}All values are within normal limits{RESET}")

        count+=1
    print(f"{BLUE}\n🖴EBS check completed🖴{RESET}")

try:
    check_ebs_usage()
except Exception as e:
    print(f"Something went wrong: {e}")   
