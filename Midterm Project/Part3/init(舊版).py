import boto3
import msgpackrpc
import time
import subprocess

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

def create_ring(my_ip):
    client = new_client(my_ip, 5057)
    client.call("create")
    time.sleep(2)

def join_node(my_ip, target_ip):
    # print("join node...")
    client_1 = new_client(target_ip, 5057) # who help to join
    client_2 = new_client(my_ip, 5057) # the new node

    c1_info = client_1.call("get_info")
    client_2.call("join", c1_info)

def is_alive_node(targer_ip):
    client = new_client(targer_ip, 5057)
    try:
        c_info = client.call("get_info")
        if c_info[0] != b'':
            print("c_info[0]:", c_info[0], "type:", type(c_info[0]))
        else:
            return False
    except Exception as e:
        print("Non-alive node:", targer_ip)
        return False
    
    return True

def get_ec2_ips(is_including_self=True): # including self ip?
    ec2_ip = []
    ec2 = boto3.client('ec2', region_name='ap-southeast-2')
    response = ec2.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if 'PrivateIpAddress' in instance: # if the EC2 is terminated, it will not have the private ip
                # print("instance:", instance, "\n\n")
                if is_including_self:
                    ec2_ip.append(instance['PrivateIpAddress'])
                else:
                    if instance['PrivateIpAddress'] != my_ip:
                        ec2_ip.append(instance['PrivateIpAddress'])

    return ec2_ip

def get_node_ips():  
    ec2_ips = get_ec2_ips(is_including_self=True) # 因為 chunk 要平均分配給所有 node，包含自己
    node_ips = []
    for ip in ec2_ips:
        if(is_alive_node(ip)):
            node_ips.append(ip)

    return node_ips

### initial chord ###
# my_ip = os.environ.get('CHORD_IP')
my_ip = subprocess.check_output(["curl", "-s", "http://169.254.169.254/latest/meta-data/local-ipv4"]).decode('utf-8')
print("my_ip:", my_ip)
process = subprocess.Popen(["/home/ec2-user/chord", my_ip, "5057", "&"])
process.poll()
time.sleep(4)

### find the candidate target ###
# target_ip = []
# ec2 = boto3.client('ec2', region_name='ap-southeast-2')
# response = ec2.describe_instances()

# for reservation in response['Reservations']:
    
#     for instance in reservation['Instances']:
#         if 'PrivateIpAddress' in instance: # if the EC2 is terminated, it will not have the private ip
#             # print("instance:", instance, "\n\n")
#             if instance['PrivateIpAddress'] != my_ip:
#                 target_ip.append(instance['PrivateIpAddress'])


# # print("my ip:", my_ip)
# print("target ip:", target_ip)

def get_node_index(my_ip, node_ips):
    index = 0
    for node_ip in node_ips:
        if node_ip == my_ip:
            return index
        else:
            index += 1


node_ips = get_node_ips()
print("node ip:", node_ips)
if my_ip == node_ips[0]:
    print("create!")
    create_ring(my_ip)
else:
    index = get_node_index(my_ip, node_ips)

    print("join", node_ips[index-1])
    join_node(my_ip, node_ips[index-1])

# isJoin = False
# for ip in target_ip:
#     if(is_alive_node(ip)):
#         print("Alive:", ip)
#         print("join", ip)
#         # create_ring(my_ip)
#         join_node(my_ip, ip)
#         isJoin = True
#         break
#     else:
#         print("non-Alive:", ip)

# if not isJoin:
#     print("create!")
#     create_ring(my_ip)