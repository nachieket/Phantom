import boto3

boto3.setup_default_session(
	aws_access_key_id='AKIAVFK6UURB6VTP6LOJ',
	aws_secret_access_key='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',
	region_name='eu-west-2')

ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')

all_vpcs = ec2client.describe_vpcs()

for each_vpc in all_vpcs['Vpcs']:
	subnets = []

	thisvpc = ec2resource.Vpc(each_vpc["VpcId"])

	subnet_iterator = thisvpc.subnets.all()

	for each_subnet in subnet_iterator:
		print(each_subnet.subnet_id)
