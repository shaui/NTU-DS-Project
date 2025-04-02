import boto3
# import msgpackrpc
import os

# def new_client(ip, port):
# 	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

def create_ring():
    print("create ring...")

def join_node(my_ip, target_ip):
    print("join node...")
    # client_1 = new_client(target_ip, 5057) # who help to join
    # client_2 = new_client(my_ip, 5057) # the new node

    # c1_info = client_1.call("get_info")
    # client_2.call("join", c1_info)

my_ip = os.environ.get('CHORD_IP')
target_ip = ""

ec2 = boto3.client('ec2', region_name='us-east-1')
response = ec2.describe_instances()

for reservation in response['Reservations']:

    for instance in reservation['Instances']:

        if instance['PrivateIpAddress'] != my_ip:
            
            target_ip = instance['PrivateIpAddress']
            # join_node()
            break
    else:
        continue
    break

print("my ip:", my_ip)
print("target ip:", target_ip)

if target_ip == "":
    create_ring()

