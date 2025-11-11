import boto3
import requests
import json
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


region = "ap-south-1"
threshold = 80.0

secret_name='Telegram_bot_secrets'
secrets_client = boto3.client("secretsmanager", region_name=region)
secret_response = secrets_client.get_secret_value(SecretId=secret_name)
secret_dict = json.loads(secret_response["SecretString"])

TELEGRAM_BOT_TOKEN = secret_dict["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = secret_dict["TELEGRAM_CHAT_ID"]


def get_instances():
    instances=[]
    ec2=boto3.client('ec2', region_name=region)
    response = ec2.describe_instances(Filters=[{"Name":"instance-state-name","Values":["running"]}])
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance["InstanceId"])
    return instances


    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/get_metric_statistics.html
    
def get_cpu_utilization(instance_id):
    end_time = datetime.now(timezone.utc)
    start_time= end_time - timedelta(minutes=5)
    client = boto3.client('cloudwatch', region_name=region)
    metrics= client.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=[
            'Average',
        ],
        ExtendedStatistics=[
            'p95',
        ],
        Unit='Percent'
    )
        
    datapoints = metrics["Datapoints"]
    if len(datapoints) > 0:
        last_point=datapoints[-1]
        return last_point["Average"]
    else:
        return None

def send_telegram_alert(instance_id, region, cpu_value):
    message= (f"🚨High CPU usage🚨 \n Instance: {instance_id}\n Region '{region}'\n CPU utilization: {cpu_value:.2f}%⚠️\n Timestamp: '{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}'")

    url= f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

    # https://core.telegram.org/bots/api#sendmessage

def main():
    instances = get_instances()
    if not instances:
        print("No running instances found")

    for instance_id in instances:
        cpu_value = get_cpu_utilization(instance_id)
        if cpu_value is None:
            continue
        print(f"{BLUE}Instance:{RESET} '{instance_id}', {CYAN}CPU utilization:{RESET} '{cpu_value:.2f}%'")

        if cpu_value > threshold:
            print(f"🚨{RED}Sending alerts for Instance:{RESET} {instance_id}, {RED}CPU utilization:{RESET} {cpu_value:.2f}%⚠️")
            send_telegram_alert(instance_id, region, cpu_value)

try:
    main()
except Exception as e:
    print(f"Something went wrong: {e}")
