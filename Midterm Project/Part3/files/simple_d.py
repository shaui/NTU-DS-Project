import requests
import sys

file_name = sys.argv[1]
ip = sys.argv[2]

def simple_download(filename, ip): # 參考助教 part2 test_download.py，不用 hash 找 node，直接從指定 IP 下載
    print("Downloading file from http://{}".format(ip))
    response = requests.get("http://{}:5058/{}".format(ip, filename))
    print("Response:", response, "Status:", response.status_code)

    # with open(filename, "wb") as f:
    #     f.write(response.content)

simple_download(file_name, ip)