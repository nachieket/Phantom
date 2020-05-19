#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import re


class PrismaAccessParser(object):
	"""Class for general methods and attributes"""

	def __init__(self):
		self.prisma_access_vars = {}

	def format_prisma_access_dict(self, csv, section):
		"""Method to input all parameters in to Prisma Access Dictionary"""

		self.prisma_access_vars[section] = {}

		csv.readline()
		csv.readline()

		for line1 in csv:
			if 'Section End' in line1:
				break
			elif re.match(r',,', line1):
				continue
			elif re.match(r'## .+ ##.*', line1):
				continue
			elif re.match(r'(.+),"(.+)"', line1):
				catch1 = re.match(r'(.+),"(.+)"', line1)
				self.prisma_access_vars[section][catch1.group(1)] = catch1.group(2)
			elif re.match(r'(.+),"(.+)', line1):
				catch1 = re.match(r'(.+),"(.+)"{0}', line1)
				self.prisma_access_vars[section][catch1.group(1)] = []
				self.prisma_access_vars[section][catch1.group(1)].append(catch1.group(2))

				for line2 in csv:
					if re.match(r'(.+)"', line2):
						catch2 = re.match(r'(.+)"', line2)
						self.prisma_access_vars[section][catch1.group(1)].append(catch2.group(1))

						break
					elif re.match(r'(.+)', line2):
						catch2 = re.match(r'(.+)', line2)
						self.prisma_access_vars[section][catch1.group(1)].append(catch2.group(1))
			elif re.match(r'(.+)', line1):
				catch1 = re.match(r'(.+)', line1)
				catch1 = catch1.group(1).split(',')
				self.prisma_access_vars[section][catch1[0]] = catch1[1]

	def parse_input_file(self, filename):
		"""Method to pull all information from csv file"""

		try:
			csv = open(filename, 'r')
		except Exception as e:
			print('input csv file cannot be opened. Terminating the program. - {}'.format(e))
			exit(-1)
		else:
			for line in csv:
				if 'Panorama Section' in line:

					self.format_prisma_access_dict(csv, 'Panorama')
				if 'AWS Section' in line:

					self.format_prisma_access_dict(csv, 'AWS')
				if 'Azure Section' in line:

					self.format_prisma_access_dict(csv, 'Azure')
				elif 'Authentication Section' in line:

					self.format_prisma_access_dict(csv, 'Authentication')
				elif 'Service Connection Setup Section' in line:

					self.format_prisma_access_dict(csv, 'Service_Connection_Setup')
				elif 'Service Connections Section' in line:

					self.format_prisma_access_dict(csv, 'Service_Connections')
				elif 'Mobile Users Portal Configuration Section' in line:

					self.format_prisma_access_dict(csv, 'Mobile_User_Portal')
