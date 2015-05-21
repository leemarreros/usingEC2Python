import boto

# AMAZON WEB SERVICES Programming
Set of scripts that allows the user to:
# 1	–  Create an EC2 instance running a choice of at least2 different AMIs
# 2	–  List the number of running EC2 instances and AMI types you currently have running
# 3	–  Suspend/restart one of your EC2 instances – Terminate an EC2 instance


# SCRIPTS



# 111111111111111111111111111111111111111111111111111111111111111111111111111111111111
# 1	–  Create an EC2 instance running a choice of at least2 different AMIs

# In order to set up an EC2 it is required four previos steps:

# i.  Sign Up for AWS
# ii. Create an IAM User
# iii.Create a Key Pair
# iv. Create a Virtual Private Cloud (VPC)
# v.  Create a Security Group

# After we sign up, we need to get the keys (public and private) via AWS console
aws_access_key_id = raw.input('Provide your Acces Key')
aws_secret_access_key = raw.input('Provide your secret acces key')

#Connecting to IAM
iam = boto.connect_iam(aws_access_key_id, aws_secret_access_key)

#Creating a group
iam.create_group('awsFinalProject')

#Adding policy to the group
policy_json='''{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}'''
iam.put_group_policy('awsFinalProject','allow-all', policy_json)

#Creating a new user
iam.create_user('finprojectuser')

#Adding users to a  group
iam.add_user_to_group('awsFinalProject','finprojectuser')

#Creating key Pair
ec2 = boto.connect_ec2()
key = ec2.create_key_pair('keypfinalaws')
import os
key.save(os.getcwd())

#Since this is a Virtual Private Cloud by defaul, there is no need to create it again.

#Creating a security group
secg = ec2.create_security_group('groupawsfinalp','Group made for Final Project')

#Auhorizating tcp 22
secg.authorize('tcp', 22, 22, cidr_ip="24.6.220.41/32")
secg.authorize('tcp', 80, 80, cidr_ip="24.6.220.41/32")

#So far, we have all the requirements to launch a EC2 instance.

#Let's find some Images to use:
#Some filters has been used to reduces the huge amount of ami's.
listami = ec2.get_all_images(filters = {'architecture': 'i386', 'root-device-type':'ebs', 'virtualization-type':'paravirtual', 'owner-alias':'amazon'})
listami[:4]

#launching with an ami we got from the lit.
ec2.run_instances('ami-0380356a',key_name='keypfinalaws',instance_type = 't1.micro',security_groups = ['groupawsfinalp'])



# 22222222222222222222222222222222222222222222222222222222222222222222222222222222222222
# 2	–  List the number of running EC2 instances and AMI types you currently have running

#Displaying all the instances and its quantity:
ec2.get_all_instances()
len(ec2.get_all_instances())

#Displaying the type of instances:
# http://www.saltycrane.com/blog/2010/03/how-list-attributes-ec2-instance-python-and-boto/
reservations = ec2.get_all_intances()
instances = [i for r in reservations for i in r.instances]
for i in instances:
    print(i.__dict__)



# 333333# 333333# 333333# 333333# 333333# 333333# 333333# 333333# 333333# 333333# 333333# 333333
# 3	–  Suspend/restart one of your EC2 instances – Terminate an EC2 instance

#Stop instances
#The value 'i-9143fb46' has been found at instances[0]
ec2.stop_instances(instance_ids=['i-9143fb46'])

#Start instances
instances[0].start

#Terminating instances:
#The value 'i-fa0bb32b' has been found at intances[1]
ec2.terminate_instances(instance_ids=['i-9143fb46', 'i-fa0bb32b'])

