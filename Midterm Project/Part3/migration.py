# 固定 1 分鐘執行一次
import time
import sys
import time
import subprocess
import msgpackrpc
import hashlib

file_name = sys.argv[0]
# file_names = get_file_names()
my_ip = subprocess.check_output(["curl", "-s", "http://169.254.169.254/latest/meta-data/local-ipv4"]).decode('utf-8')

def new_client(ip, port):
	return msgpackrpc.Client(msgpackrpc.Address(ip, port))

def hash(str):
	return int(hashlib.md5(str.encode()).hexdigest(), 16) & ((1 << 32) - 1)

def isNeedMigrate(my_ip, file_name):

    # 確認一下 hash upload 這一段
    filepath = filename
    slashs = [i for i, c in list(enumerate(filepath)) if c == '/']
    if len(slashs) != 0:
        filename = filename[max(slashs) + 1:]

    client = new_client(my_ip, 5057)
    h = hash(filename)
    print("Hash of {} is {}".format(filename, h))

    node = client.call("find_successor", h)
    node_ip = node[0].decode()

    if node_ip != my_ip: # 找到新的存放位置，要 migration
         return True
    else:
         return False

def migrate():
    # simple_upload(ip, file_name)

    # delete the file
    pass

while True:
    if not isNeedMigrate(my_ip, file_name):
        time.sleep(60)
    else:
        migrate()
        break
