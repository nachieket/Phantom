import boto3

boto3.setup_default_session(
	aws_access_key_id='AKIAVFK6UURB6VTP6LOJ',
	aws_secret_access_key='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',
	region_name='eu-west-2')

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
