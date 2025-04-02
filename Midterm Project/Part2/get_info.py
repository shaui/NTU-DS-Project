import msgpackrpc

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))


ip = "172.31.28.72"
client = new_client(ip, 5057)

print("target:", client.call("get_info"))
print("predecessor:", client.call("get_predecessor"))
print("successor:", client.call("get_successor", 0))