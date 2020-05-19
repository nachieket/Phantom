#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import xml.etree.ElementTree as Et
from time import sleep

from .Status.Status import Status
from .PasswordChange.PasswordChange import PasswordChange
from .GetAPIKey.GetAPIKey import GetAPIKey
from ....API.XMLX.XMLX import XMLX
from ....Logger.PanoramaGenericLogger.PanoramaGenericLogger import PanoramaGenericLogger as PanoramaLogger


class Operations(Status, PasswordChange, GetAPIKey):
	"""
	Panorama class
	"""

	def __init__(self):
		# print('++++ Panorama Operations Class')
		super().__init__()
		super(Status, self).__init__()
		super(PasswordChange, self).__init__()
		# print('---- Panorama Operations Class')

	@staticmethod
	def set_panorama_serial(panorama_ip, api_key, license_serial):
		"""
		Method to set Panorama serial number

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:param license_serial:
		:type license_serial:
		:return: None
		:rtype: None
		"""

		xmx = XMLX()

		uri = 'https://%s/api/?type=op&cmd=<set><serial-number>%s</serial-number></set>&key=%s'

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri % (panorama_ip, license_serial, api_key), logger=PanoramaLogger.panorama,
				type_='License Serial', name='Panorama', ops='yes', smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)
			return tree.attrib['status']

	@staticmethod
	def fetch_panorama_license(panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:return:
		:rtype:
		"""

		xmx = XMLX()
		features = {}

		uri = 'https://%s/api/?type=op&cmd=<request><license><fetch/></license></request>&key=%s'

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri % (panorama_ip, api_key), logger=PanoramaLogger.panorama,
				type_='Fetch License', name='Panorama', ops='yes', smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			licenses = tree.findall('result/licenses/entry')

			for lic in licenses:
				feature = lic.find('feature').text
				description = lic.find('description').text

				features[feature] = description

			return features

	@staticmethod
	def request_panorama_software_check(panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:return:
		:rtype:
		"""

		versions = {}
		xmx = XMLX()

		uri = (
			'https://%s/api/?type=op&cmd=<request><system><software><check/></software></system>'
			'</request>&key=%s' % (panorama_ip, api_key)
		)

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri, logger=PanoramaLogger.panorama, type_='Software Check', name='Panorama', ops='yes',
				smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			version_list = tree.findall('result/sw-updates/versions/entry')

			for ver in version_list:
				versions[ver.find('version').text] = ver.find('filename').text

			return versions

	@staticmethod
	def request_panorama_software_download(panorama_ip, api_key, version):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:param version:
		:type version:
		:return:
		:rtype:
		"""

		xmx = XMLX()

		uri = (
			'https://%s/api/?type=op&cmd=<request><system><software><download><file>%s</file>'
			'</download></software></system></request>&key=%s'
		)

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri % (panorama_ip, version, api_key), logger=PanoramaLogger.panorama,
				type_='Software Download', name='Panorama', ops='yes', smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			jobs = tree.findall('result/job')

			for job in jobs:
				return job.text

	@staticmethod
	def request_panorama_job_status(panorama_ip, api_key, job_id):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:param job_id:
		:type job_id:
		:return:
		:rtype:
		"""

		result = 'PEND'
		status = 'ACT'
		detail = ''

		xmx = XMLX()

		uri = 'https://%s/api/?type=op&cmd=<show><jobs><id>%s</id></jobs></show>&key=%s' % (panorama_ip, job_id, api_key)

		while (status != 'FIN' and result != 'OK') or (status != 'FIN' and result != 'FAIL'):
			response = None

			while response is None or status != 'FIN':
				response = xmx.exec_xml_get(
					uri=uri, logger=PanoramaLogger.panorama,
					type_='Job Status', name='Panorama', ops='yes', smsg='Successful', fmsg='Failed'
				)

				sleep(5)

				tree = Et.XML(response.text)

				jobs = tree.findall('result/job')

				for job in jobs:
					result = job.find('result').text
					status = job.find('status').text

					detail = []
					details = job.findall('details/line')

					for line in details:
						detail.append(line.text)
		else:
			return result, detail

	@staticmethod
	def request_panorama_software_install(panorama_ip, api_key, version):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:param version:
		:type version:
		:return:
		:rtype:
		"""

		xmx = XMLX()

		uri = (
			'https://%s/api/?type=op&cmd=<request><system><software><install><version>%s</version>'
			'</install></software></system></request>&key=%s'
		)

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri % (panorama_ip, version, api_key), logger=PanoramaLogger.panorama,
				type_='Software Install', name='Panorama', ops='yes', smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			jobs = tree.findall('result/job')

			for job in jobs:
				return job.text

	@staticmethod
	def request_panorama_software_restart(panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:return:
		:rtype:
		"""

		xmx = XMLX()

		uri = 'https://%s/api/?type=op&cmd=<request><restart><system/></restart></request>&key=%s'

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri % (panorama_ip, api_key), logger=PanoramaLogger.panorama,
				type_='System Restart', name='Panorama', ops='yes', smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			return tree.attrib['status']

	@staticmethod
	def show_system_info(panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:return:
		:rtype:
		"""

		version = ''
		xmx = XMLX()

		uri = 'https://%s/api/?type=op&cmd=<show><system><info/></system></show>&key=%s'

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri % (panorama_ip, api_key), logger=PanoramaLogger.panorama,
				type_='System Info', name='Panorama', ops='yes', smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			system_info = tree.findall('result/system')

			for info in system_info:
				version = info.find('sw-version').text

			return version

	@staticmethod
	def request_plugins_check(panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:return:
		:rtype:
		"""

		xmx = XMLX()

		uri = 'https://%s/api/?type=op&cmd=<request><plugins><check/></plugins></request>&key=%s'

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri % (panorama_ip, api_key), logger=PanoramaLogger.panorama,
				type_='Plugins Check', name='Panorama', ops='yes', smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			return tree.attrib['status']

	@staticmethod
	def request_plugins_download_file(panorama_ip, api_key, plugin):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:param plugin:
		:type plugin:
		:return:
		:rtype:
		"""

		xmx = XMLX()

		uri = (
			'https://%s/api/?type=op&cmd=<request><plugins><download><file>%s</file></download>'
			'</plugins></request>&key=%s'
		)

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri % (panorama_ip, plugin, api_key), logger=PanoramaLogger.panorama,
				type_='Plugins Download', name='Panorama', ops='yes', smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			jobs = tree.findall('result/job')

			for job in jobs:
				return job.text

	@staticmethod
	def request_plugins_install(panorama_ip, api_key, plugin):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:param plugin:
		:type plugin:
		:return:
		:rtype:
		"""

		xmx = XMLX()

		uri = 'https://%s/api/?type=op&cmd=<request><plugins><install>%s</install></plugins></request>&key=%s'

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri % (panorama_ip, plugin, api_key), logger=PanoramaLogger.panorama,
				type_='Plugins Install', name='Panorama', ops='yes', smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			jobs = tree.findall('result/job')

			for job in jobs:
				return job.text

	def request_content_upgrade_download_latest(self, panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip: Panorama IP
		:type panorama_ip: str
		:param api_key: Panorama API Key
		:type api_key: str
		:return: Status
		:rtype: str
		"""

		xmx = XMLX()

		# Content Check

		uri = (
			'https://%s/api/?type=op&cmd=<request><content><upgrade><check/></upgrade></content>'
			'</request>&key=%s' % (panorama_ip, api_key)
		)

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri, logger=PanoramaLogger.panorama, type_='Content Check', name='Panorama', ops='yes',
				smsg='Successful', fmsg='Failed'
			)

			sleep(5)

		# Download

		uri = (
			'https://%s/api/?type=op&cmd=<request><content><upgrade><download><latest/></download></upgrade>'
			'</content></request>&key=%s' % (panorama_ip, api_key)
		)

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri, logger=PanoramaLogger.panorama, type_='Content Download', name='Panorama', ops='yes',
				smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			job_id = tree.find('result/job').text

		result, detail = self.request_panorama_job_status(panorama_ip=panorama_ip, api_key=api_key, job_id=job_id)

		if result == 'OK' and detail[0].rsplit('\n')[0] == 'File successfully downloaded':
			return 'success'
		else:
			return 'failure'

	@staticmethod
	def request_content_upgrade_info(panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip: Panorama IP
		:type panorama_ip: str
		:param api_key: Panorama API Key
		:type api_key: str
		:return: None
		:rtype: None
		"""

		xmx = XMLX()

		# Content Info

		uri = (
			'https://%s/api/?type=op&cmd=<request><content><upgrade><info/></upgrade></content>'
			'</request>&key=%s' % (panorama_ip, api_key)
		)

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri, logger=PanoramaLogger.panorama, type_='Content Info', name='Panorama', ops='yes',
				smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			entry = tree.findall('result/content-updates/entry')

			for e in entry:
				version = e.find('version').text
				status = e.find('downloaded').text

				if status == 'yes':
					return version

	def request_content_upgrade_install(self, panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip: Panorama IP
		:type panorama_ip: str
		:param api_key: Panorama API Key
		:type api_key: str
		:return: Status
		:rtype: str
		"""

		xmx = XMLX()

		# Content Info

		uri = (
			'https://%s/api/?type=op&cmd=<request><content><upgrade><install><version>latest</version></install>'
			'</upgrade></content></request>&key=%s' % (panorama_ip, api_key)
		)

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri, logger=PanoramaLogger.panorama, type_='Content Info', name='Panorama', ops='yes',
				smsg='Successful', fmsg='Failed'
			)

			sleep(5)
		else:
			tree = Et.XML(response.text)

			job_id = tree.find('result/job').text

		result, detail = self.request_panorama_job_status(panorama_ip=panorama_ip, api_key=api_key, job_id=job_id)

		if result == 'OK' and detail[0] == 'Configuration committed successfully':
			return 'success'
		else:
			return 'failure'

	def request_panorama_commit(self, panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:return:
		:rtype:
		"""

		count = 0
		xmx = XMLX()

		uri = 'https://%s/api?type=commit&cmd=<commit></commit>&key=%s'

		while count < 5:

			response = None

			while response is None:
				response = xmx.exec_xml_get(
					uri=uri % (panorama_ip, api_key), logger=PanoramaLogger.panorama,
					type_='Local Commit', name='Panorama', ops='yes'
				)

				sleep(5)
			else:
				tree = Et.XML(response.text)

				if tree.find('result/msg/line') is not None:
					message = tree.find('result/msg/line')

					if 'Commit job enqueued with jobid' in message.text:
						job = tree.find('result/job')

						catch = self.request_panorama_job_status(
							panorama_ip=panorama_ip, api_key=api_key, job_id=job.text
						)

						if catch[0] == 'OK':
							return 'success'
						else:
							count += 1
					else:
						count += 1
				elif tree.find('msg') is not None:
					message = tree.find('msg')

					if 'There are no changes to commit' in message.text:
						return 'success'
					else:
						count += 1

	@staticmethod
	def request_panorama_service_connection_commit(panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:return:
		:rtype:
		"""

		xmx = XMLX()

		uri = (
			"https://%s/api/?type=commit&action=all&cmd=<commit-all><shared-policy><include-template>yes"
			"</include-template><device-group><entry name='Service_Conn_Device_Group'/></device-group>"
			"</shared-policy></commit-all>&key=%s"
		)

		response = None

		while response is None:
			response = xmx.exec_xml_get(
				uri=uri % (panorama_ip, api_key), logger=PanoramaLogger.panorama,
				type_='Commit Service Connection', name='Panorama', ops='yes'
			)

			sleep(5)

	@staticmethod
	def request_panorama_remote_network_commit(panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:return:
		:rtype:
		"""

		xmx = XMLX()

		uri = (
			"https://%s/api/?type=commit&action=all&cmd=<commit-all><shared-policy><include-template>yes"
			"</include-template><device-group><entry name='Remote_Network_Device_Group'/></device-group>"
			"</shared-policy></commit-all>&key=%s"
		)

		response = xmx.exec_xml_get(
			uri=uri % (panorama_ip, api_key), logger=PanoramaLogger.panorama,
			type_='Commit Remote Network', name='Panorama', ops='yes'
		)

		print(response.text)

	@staticmethod
	def request_panorama_mobile_user_commit(panorama_ip, api_key):
		"""
		Method to fetch Panorama license

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:return:
		:rtype:
		"""

		xmx = XMLX()

		uri = (
			"https://%s/api/?type=commit&action=all&cmd=<commit-all><shared-policy><include-template>yes"
			"</include-template><device-group><entry name='Mobile_User_Device_Group'/></device-group>"
			"</shared-policy></commit-all>&key=%s"
		)

		response = xmx.exec_xml_get(
			uri=uri % (panorama_ip, api_key), logger=PanoramaLogger.panorama,
			type_='Commit Mobile User', name='Panorama', ops='yes'
		)

		print(response.text)
