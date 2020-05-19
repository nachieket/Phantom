import boto3

boto3.setup_default_session(
	aws_access_key_id='AKIAVFK6UURB6VTP6LOJ',
	aws_secret_access_key='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',
	region_name='eu-west-2')

ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')

igw_response = ec2client.describe_internet_gateways()

for each_igw in igw_response['InternetGateways']:
	this_igw = ec2resource.InternetGateway(each_igw['InternetGatewayId'])

	print(this_igw.attachments)
