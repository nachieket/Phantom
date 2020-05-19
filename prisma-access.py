#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import argparse
import datetime

from modules.PaloAltoNetworks.FileParser import FileParser
from modules.PaloAltoNetworks.Playbooks.PrismaAccess.AWSPrismaAccess.AWSPrismaAccess import AWSPrismaAccess
from modules.PaloAltoNetworks.Playbooks.PrismaAccess.AzurePrismaAccess.AzurePrismaAccess import AzurePrismaAccess
from modules.PaloAltoNetworks.Playbooks.PrismaAccess.ConfigPrismaAccess.ConfigPrismaAccess import ConfigPrismaAccess
# from ..modules.PaloAltoNetworks.Panorama.Panorama import Panorama
# from ..modules.PaloAltoNetworks.Panorama.Operations.Operations import Operations


def runtime():
	"""Function for run time parameters"""

	parser = argparse.ArgumentParser(
		usage='%(prog)s -c -f <file>', description='Prisma Access Auto Deployment'
	)

	parser.add_argument('-c', '--create', action='store_const', help='Deploy Prisma Access', const='create')
	parser.add_argument('-f', '--file', action='store', help='Prisma Access Parameters File', metavar='<FILE>')

	args = parser.parse_args()

	if args.file and args.create:
		return args.file, 'create'
	else:
		print('Incorrect set of arguments or mandatory runtime parameters are missing.')
		print('Run \'prisma-access.py -h\'.')
		print('Exiting the program.')
		exit()


def main():
	"""Prisma Access Main Method"""

	start = datetime.datetime.now()
	print('\nStart time: ', str(start), '\n')

	file, action = runtime()

	parse = FileParser.PrismaAccessParser()
	parse.parse_input_file(filename=file)

	if parse.prisma_access_vars['Panorama']['platform'] == 'Azure':
		azure_prisma_access = AzurePrismaAccess()

		azure_prisma_access.orchestrator(parameters=parse.prisma_access_vars)
	elif parse.prisma_access_vars['Panorama']['platform'] == 'AWS':
		aws_prisma_access = AWSPrismaAccess()

		aws_prisma_access.orchestrator(parameters=parse.prisma_access_vars)
	elif parse.prisma_access_vars['Panorama']['platform'] == 'VMWare':
		vmware_prisma_access = ConfigPrismaAccess()

		vmware_prisma_access.orchestrator(parameters=parse.prisma_access_vars)

	end = datetime.datetime.now()
	print('End time: ', str(end))
	print()
	print('#' * 50)
	print('\nTOTAL TIME TO COMPLETE: {}'.format(end - start))
	print()
	print('#' * 50)
	print()


if __name__ == '__main__':
	main()
