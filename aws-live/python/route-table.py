import boto3

boto3.setup_default_session(
	aws_access_key_id='AKIAVFK6UURB6VTP6LOJ',
	aws_secret_access_key='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',
	region_name='eu-west-2')

ec2client = boto3.client('ec2')
ec2resource = boto3.resource('ec2')

response = ec2client.create_vpc(CidrBlock='10.10.0.0/16')

newvpcid = response['Vpc']['VpcId']

myvpc = ec2resource.Vpc(newvpcid)

my_route_tables_iterator = myvpc.route_tables.all()

print('The VPC' + newvpcid + 'has following route tables')

for this_route_table in my_route_tables_iterator:
	print(this_route_table.id)

myvpc.delete()
