import msgpackrpc

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

client_1 = new_client("172.31.85.152", 5057)
client_1.call("create")
