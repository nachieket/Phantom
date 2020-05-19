#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import re

from .....API.XMLX.XMLX import XMLX
from ....PaloAltoNetworks import PaloAltoNetworks
from .....Logger.SettingsLogger.SettingsLogger import SettingsLogger as SLogger


class Template(PaloAltoNetworks):
	"""
	Class to configure Panorama Template
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ Template')
		super().__init__(panorama_ip, api_key)
		# print('---- Template')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Panorama template xpath and element to place in API request string

		:return: xpath and element (XML code)
		:rtype: tuple
		"""

		xpath = "/config/devices/entry[@name='localhost.localdomain']"

		element = """
				<template>
					<entry name="%s">
						<settings>
						<default-vsys>vsys1</default-vsys>
						</settings>
						<config>
						<devices>
							<entry name="localhost.localdomain">
							<vsys>
								<entry name="vsys1"/>
							</vsys>
							</entry>
						</devices>
						</config>
					</entry>
				</template>
			"""

		return xpath, re.sub(r'\s\s+|\n', '', element)

	def add_template(self, template):
		"""
		Method to configure a template in Panorama

		Example: add_template('Sample')

		:param template: a template to configure
		:type template: str
		:return: None
		:rtype: None
		"""

		xmx = XMLX()

		xpath, element = self.__xcode()

		try:
			uri = xmx.configure.format(self.panorama_ip, xpath, element % template, self.api_key)
		except Exception as e:
			SLogger.settings.info('Template: {} - {}'.format(template, e))
		else:
			xmx.exec_xml_get(uri, SLogger.settings, 'Template', template)
