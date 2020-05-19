import boto3

boto3.setup_default_session(
	aws_access_key_id='AKIAVFK6UURB6VTP6LOJ',
	aws_secret_access_key='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',
	region_name='eu-west-2')


# Create client and use parameters from default session

# ec2client = boto3.client('ec2')

# Create client and use own parameters

# ec2client = boto3.client(
# 	'ec2',
# 	aws_access_key_id='AKIAVFK6UURB6VTP6LOJ',
# 	aws_secret_access_key='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',
# 	region='eu-west-2'
# )

# # Create client and create VPC with CIDR Block
#
# ec2client = boto3.client('ec2')
# ec2resource = boto3.resource('ec2')
#
# response = ec2client.create_vpc(CidrBlock='10.10.0.0/16')
#
# # Get the VPC ID and pass it to ec2resource.Vpc to create a VPC Class
#
# newvpcid = response['Vpc']['VpcId']
#
# newvpc = ec2resource.Vpc(newvpcid)
#
# print(newvpc.vpc_id)
# print(newvpc.cidr_block)
# print(newvpc.state)
#
# # Pull the list of all instances and show all with for loop
#
# thelist = newvpc.instances.all()
#
# for instance in thelist:
# 	print(instance)
#
# # Attach to Gateway
# # newvpc.attach_internet_gateway(InternetGatewayId="igw-123456")
#
# # Delete a VPC using VPC Class
# newvpc.delete()

# print(response.vpc_id)

# ec2resource = boto3.resource('ec2')
#
# new_vpc_object = ec2resource.create_vpc(CidrBlock='10.10.0.0/16')
#
# print(new_vpc_object.vpc_id)

ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')

vpc_info = []
all_vpcs = ec2client.describe_vpcs()
all_subnets = ec2client.describe_subnets()

for each_vpc in all_vpcs['Vpcs']:
	subnets = []

	for each_subnet in all_subnets['Subnets']:
		if each_subnet['VpcId'] == each_vpc['VpcId']:
			subnets.append([each_subnet['CidrBlock'], each_subnet['AvailabilityZone']])

	obj = ec2resource.Vpc(each_vpc['VpcId'])
	vpc_info.append((each_vpc['Tags'][0]['Value'], obj.vpc_id, obj.cidr_block, obj.state, subnets))

for each_vpc in vpc_info:
	print(each_vpc)

# all_subnets = ec2client.describe_subnets()

# for each_subnet in all_subnets['Subnets']:
# 	print(each_subnet)

# for each_vpc in newvpc:
# 	print(each_vpc.vpc_id, '-', each_vpc.cidr_block, '-', each_vpc.state)
