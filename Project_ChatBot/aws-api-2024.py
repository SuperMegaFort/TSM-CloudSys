# Creator: Francisco Mendonca (francisco.mendonca@hesge.ch)

import boto3
import os
import time


# Before starting, in the command line do:
#  aws configure
# and fill up the required keys.


EC2_RESOURCE = boto3.resource('ec2', region_name='us-east-1')
EC2_CLIENT = boto3.client('ec2',region_name='us-east-1')
S3_CLIENT = boto3.client('s3', region_name='us-east-1')
S3_RESOURCE = boto3.resource('s3', region_name='us-east-1')

# Difference between Client and Resource:
# Client: low-level service access
# Resource: higher-level object-oriented service access
#  The main difference is the way we interact with the AWS API.
#  While both can do mostly the same things, sometimes it's faster to use Clients, and others it's faster to use Resources.

print("Creating Instance...")

# Create a new EC2 instance
new_instance = EC2_RESOURCE.create_instances(
    ImageId='ami-02e136e904f3da870',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro'
)

# Changing name of an instance
EC2_RESOURCE.create_tags(Resources=[new_instance[0].id], Tags=[
    {
        'Key': 'Name',
        'Value': "AWS-Instance",
    },
])


print("Instances Created")
for instance in new_instance:
    print(instance)

new_instance[0].wait_until_running()
 # Waiting for the instances to be active

input("Your instance is now Ready. Press any button.")

# Prints all running instances.

for status in EC2_CLIENT.describe_instance_status()['InstanceStatuses']:
    print(status['InstanceId'], ': ', status["InstanceState"]["Name"])


# # Delete Instance
for instance in new_instance:
    print("Deleting Instance: ", instance)
    instance.terminate()

## S3

# Create Bucket

# The bucket name for AWS has to be different from other IaaS, 
#  as the original name brought up aerror

print("Creating Bucket")
response = S3_CLIENT.create_bucket(
    Bucket='lsds-aws-bucket-2023',
)


print(response)
print()

# # Push to Bucket

# # # first create an empty file, if a file with the same name doens't exist.
if not os.path.isfile("file-to-upload.txt"):
    open('file-to-upload.txt', 'a').close()

print("Writing Item to Bucket")
response = S3_CLIENT.put_object(
    Body='file-to-upload.txt',
    Bucket='lsds-aws-bucket-2023',
    Key='file-in-bucket.txt',
)

input('Check bucket for success. Press button when done.')

print(response,'\n')
# # # Download File to current directory
print("Downloading file from Bucket")
S3_CLIENT.download_file('lsds-aws-bucket-2023', 'file-in-bucket.txt', 'downloaded-file.txt')


# # # Delete Bucket

# First, delete all objects in the Bucket
bucket = S3_RESOURCE.Bucket('lsds-aws-bucket-2023')

print("Deleting all objects in Bucket\n")
bucket.objects.all().delete()


print("Deleting Bucket")
# Bucket Deletion
response = S3_CLIENT.delete_bucket(
    Bucket='lsds-aws-bucket-2023'
)

print(response)