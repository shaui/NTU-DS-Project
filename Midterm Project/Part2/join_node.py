import msgpackrpc


def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

my_ip = "172.31.89.224"
target_ip = "172.31.85.152"

client_1 = new_client(target_ip, 5057) # who help to join
client_2 = new_client(my_ip, 5057) # the new node

c1_info = client_1.call("get_info")
client_2.call("join", c1_info)