#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import re

from .....API.XMLX.XMLX import XMLX
from ....PaloAltoNetworks import PaloAltoNetworks
from .....Logger.SettingsLogger.SettingsLogger import SettingsLogger as SLogger


# TODO: Add code to add firewalls to Template STack


class TemplateStack(PaloAltoNetworks):
	"""
	Class to configure Panorama Template Stack
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ TemplateStack')
		super().__init__(panorama_ip, api_key)

		# print('---- TemplateStack')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode(caller):
		"""
		Method to return Panorama template-stack xpath and element to place in API request string

		:param caller: Caller of this method; decides what to return
		:type caller: str
		:return: xpath, member xpath, element (XML code) and member element (XML code)
		:rtype: tuple
		"""

		xpath = "/config/devices/entry[@name='localhost.localdomain']"

		mxpath = "/config/devices/entry[@name='localhost.localdomain']/template-stack/entry[@name='%s']"

		element = """
					<template-stack>
						<entry name="%s">
							<settings/>
						</entry>
					</template-stack>
				"""

		melement = """
					<templates>
						<member>%s</member>
					</templates>
				"""

		fwelement = """
					<devices>
						<entry name="%s"/>
					</devices>
				"""

		if caller == 'template_stack':
			return xpath, re.sub(r'\s\s+|\n', '', element)
		elif caller == 'add_template':
			return mxpath, re.sub(r'\s\s+|\n', '', melement)
		elif caller == 'add_firewall':
			return mxpath, re.sub(r'\s\s+|\n', '', fwelement)

	def add_template_stack(self, template_stack):
		"""
		Method to configure a template stack and optionally add templates to it

		Example: add_template_stack(template_stack='SampleStack')

		:param template_stack: Template Stack to configure
		:type template_stack: str
		:return: None
		:rtype: None
		"""

		xmx = XMLX()

		xpath, element = self.__xcode('template_stack')

		try:
			uri = xmx.configure.format(
				self.panorama_ip, xpath, element % template_stack, self.api_key
			)
		except Exception as e:
			SLogger.settings.info('Template-Stack: {} - {}'.format(template_stack, e))
		else:
			xmx.exec_xml_get(uri, SLogger.settings, 'Template-Stack', template_stack)

	def add_template_to_template_stack(self, template_stack, templates):
		"""
		Method to add one or more templates to template stack

		Example: add_template_to_template_stack(template_stack='SampleStack', templates=['Sample1', 'Sample2'])

		:param template_stack: Template stack name
		:type template_stack: str
		:param templates: List of all templates to add to a stack
		:type templates: list
		:return: None
		:rtype: None
		"""

		smsg = 'Successfully added template'
		fmsg = 'Failed to add template'

		xmx = XMLX()

		mxpath, melement = self.__xcode('add_template')

		for template in templates:
			try:
				uri = xmx.configure.format(
					self.panorama_ip, mxpath % template_stack, melement % template, self.api_key
				)
			except Exception as e:
				SLogger.settings.info('Template-Stack: {} - {}'.format(template_stack, e))
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'Template-Stack', template_stack, smsg, fmsg)

	def add_fw_to_template_stack(self, template_stack, firewalls):
		"""
		Method to add one or more firewalls to template stack

		Example: add_fw_to_template_stack(template_stack='SampleStack', firewalls=['015351000024056'])

		:param template_stack: Template stack name
		:type template_stack: str
		:param firewalls: List of all firewalls to add to a stack
		:type firewalls: list
		:return: None
		:rtype: None
		"""

		smsg = 'Successfully added firewall'
		fmsg = 'Failed to add firewall'

		xmx = XMLX()

		mxpath, fwelement = self.__xcode('add_firewall')

		for firewall in firewalls:
			try:
				uri = xmx.configure.format(
					self.panorama_ip, mxpath % template_stack, fwelement % firewall, self.api_key
				)
			except Exception as e:
				SLogger.settings.info('Template-Stack: {} - {}'.format(template_stack, e))
			else:
				xmx.exec_xml_get(uri, SLogger.settings, 'Template-Stack', template_stack, smsg, fmsg)
