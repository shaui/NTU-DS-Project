import os
import time

dir_path = "/home/ec2-user/files"

while True:
    file_list = os.listdir(dir_path)
    sleep_time = 30

    print("file_list:", file_list)

    time.sleep(sleep_time)