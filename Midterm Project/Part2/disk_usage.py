import boto3

# 建立 EC2 client
ec2_client = boto3.client('ec2')

# 建立 Auto Scaling client
asg_client = boto3.client('autoscaling')

# 取得 Auto Scaling Group 詳細資料
response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=['myAuto'])

# 取得 Auto Scaling Group 內所有 EC2 instance ID
instance_ids = []
for instance in response['AutoScalingGroups'][0]['Instances']:
    instance_ids.append(instance['InstanceId'])

print("instance_ids:", instance_ids)
# 取得 instance 詳細資料，包含 disk 使用率
for instance_id in instance_ids:
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    for block_device in response['Reservations'][0]['Instances'][0]['BlockDeviceMappings']:
        if 'Ebs' in block_device:
            volume_id = block_device['Ebs']['VolumeId']

            vol_device = ec2_client.describe_volumes(VolumeIds=[volume_id])["Volumes"][0]["Attachments"][0]["Device"]
            vol_size = ec2_client.describe_volumes(VolumeIds=[volume_id])["Volumes"][0]["Size"]
            print("vol_device:", vol_device, "vol_size:", vol_size)
