import boto3
import subprocess
my_ip = subprocess.check_output(["curl", "-s", "http://169.254.169.254/latest/meta-data/local-ipv4"]).decode('utf-8')

### find the candidate target ###
# target_ip = ""
target_ip = []
ec2 = boto3.client('ec2', region_name='us-east-1')
response = ec2.describe_instances()

for reservation in response['Reservations']:

    for instance in reservation['Instances']:

        if instance['PrivateIpAddress'] != my_ip:
            print("instance:", instance)
            # target_ip = instance['PrivateIpAddress']
            target_ip.append(instance['PrivateIpAddress'])
    #         break
    # else:
    #     continue
    # break

print("target_ip:", target_ip)