import requests
import time
import random

def download():
  print("dn")
  API = "http://final-lb-2110684570.us-east-1.elb.amazonaws.com:5000/download_remote?name=107-國企系-邁向Elite之路管院生的面試手冊.doc"
  r = requests.get(API)
  print(r.content[0:100])
def browse():
  print("br")
  API = "http://final-lb-2110684570.us-east-1.elb.amazonaws.com:5000/preview_remote?name=107-國企系-邁向Elite之路管院生的面試手冊.doc"
  r = requests.get(API)
  print(r.content[0:100])
  

timestamp = 0.1
round_of_call = 1
num_of_call = 100

random.seed(777)
calls = [download, browse]

for _ in range(round_of_call):
  for i in range(num_of_call):
    call = random.choice(calls)
    call()
  time.sleep(timestamp)
