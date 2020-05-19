import boto3

boto3.setup_default_session(
	aws_access_key_id='AKIAVFK6UURB6VTP6LOJ',
	aws_secret_access_key='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',
	region_name='eu-west-2')

ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')

response = ec2client.create_internet_gateway()

newigwid = response["InternetGateway"]["InternetGatewayId"]

newigw = ec2resource.InternetGateway(newigwid)

# new_igw_object = ec2resource.create_internet_gateway()

# newigw.attach_to_vpc(
# 	VpcId=newvpcid
# )
