#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3


class Miscellaneous(object):
	"""Class for general methods and attributes"""
	
	def __init__(self):
		self.tgw = {}
		self.vals = {}

	def format_tgw_dict(self, line, csv, section):
		"""Method to input all parameters in to TGW Dictionary"""

		self.tgw[section] = {}
		configure = line.split(',')[1].split(':')[1].lower().rsplit('\n')[0]

		if configure == 'yes':
			self.tgw[section]['Configure'] = 'Yes'
		elif configure == 'no':
			self.tgw[section]['Configure'] = 'No'

		csv.readline()
		csv.readline()

		if section == 'Panorama':
			location = csv.readline()
			self.tgw[section][location.split(',')[0]] = location.split(',')[1].rsplit('\n')[0]

			line = csv.readline()
			self.tgw[section][line.split(',')[0]] = line.split(',')[1].rsplit('\n')[0]

			if self.tgw[section]['Configure'] == 'Yes' and 'services-vpc' in location.lower():
				for line in csv:
					if 'Section End' in line:
						break
					elif 'authcode' in line.split(',')[0]:
						self.tgw[section][line.split(',')[0]] = line.split(',')[1].rsplit('\n')[0]
					elif (line.split(',')[0] and line.split(',')[1].rsplit('\n')[0]) == '':
						pass
					else:
						self.tgw[section][line.split(',')[0]] = line.split(',')[1].rsplit('\n')[0]
						self.vals[line.split(',')[0]] = line.split(',')[1].rsplit('\n')[0]
			elif self.tgw[section]['Configure'] == 'Yes' and 'on-premise' in location.lower():
				for line in csv:
					if 'Section End' in line:
						break
					elif 'mgmtpanoramaip' in line.split(',')[0]:
						self.tgw[section][line.split(',')[0]] = line.split(',')[1].rsplit('\n')[0]
					elif (line.split(',')[0] and line.split(',')[1].rsplit('\n')[0]) == '':
						pass
			else:
				for line in csv:
					if 'Section End' in line:
						break
		else:
			if self.tgw[section]['Configure'] == 'Yes':
				for line in csv:
					if 'Section End' in line:
						break
					elif 'authcode' in line.split(',')[0]:
						self.tgw[section][line.split(',')[0]] = line.split(',')[1].rsplit('\n')[0]
					elif (line.split(',')[0] and line.split(',')[1].rsplit('\n')[0]) == '':
						pass
					else:
						self.tgw[section][line.split(',')[0]] = line.split(',')[1].rsplit('\n')[0]
						self.vals[line.split(',')[0]] = line.split(',')[1].rsplit('\n')[0]
			elif self.tgw[section]['Configure'] == 'No':
				for line in csv:
					if 'Section End' in line:
						break

	def parse_input_file(self, filename):
		"""Method to pull all information from csv file"""

		try:
			csv = open(filename, 'r')
		except Exception as e:
			print('input csv file cannot be opened. Terminating the program. - {}'.format(e))
			exit(-1)
		else:
			for line in csv:
				if 'Provider Section' in line:

					self.format_tgw_dict(line, csv, 'Provider')
				elif 'S3 Section' in line:

					self.format_tgw_dict(line, csv, 'S3')
				elif 'Services-VPC Section' in line:

					self.format_tgw_dict(line, csv, 'Services')
				elif 'Panorama Section' in line:

					self.format_tgw_dict(line, csv, 'Panorama')
				elif 'LoadBalancer Section' in line:

					self.format_tgw_dict(line, csv, 'LB')
				elif 'spoke_vpc1 Section' in line:

					self.format_tgw_dict(line, csv, 'Vpc1')
				elif 'spoke_vpc2 Section' in line:

					self.format_tgw_dict(line, csv, 'Vpc2')
				elif 'Security-In-VPC Section' in line:

					self.format_tgw_dict(line, csv, 'security-In')
				elif 'Security-Out-VPC Section' in line:

					self.format_tgw_dict(line, csv, 'security-Out')
				elif 'Security-East-West-VPC Section' in line:

					self.format_tgw_dict(line, csv, 'security-East-West')
				elif 'Customer-Gateway-Variables Section' in line:

					self.format_tgw_dict(line, csv, 'CGW')
				elif 'Transit-Gateway Section' in line:

					self.format_tgw_dict(line, csv, 'TGW')
