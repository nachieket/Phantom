#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import re


class XMLPanorama(object):
	"""
	Class with all Panorama XML XPaths and Elements
	"""

	# @staticmethod
	# def move_security_rule():
	# 	"""
	# 	Method to return Panorama xpath to place in API request string to move security rule
	# 	:return: xpath
	# 	"""
	# 	xpath = (
	# 		"/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='%s"
	# 		"']/pre-rulebase/security/rules/entry[@name='%s']"
	# 	)
	#
	# 	return xpath


class XMLFirewall(object):

	@staticmethod
	def nat_rule():
		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/rulebase/nat/rules"
		)

		element = """
			<entry name="%s">
				<to>
					<member>%s</member>
				</to>
				<from>
					<member>%s</member>
				</from>
				<source>
					%s
				</source>
				<destination>
					%s
				</destination>
				<service>%s</service>
			</entry>
		"""

		return xpath, re.sub(r'\s\s+|\n', '', element)

	@staticmethod
	def move_nat_rule():
		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/rulebase/nat/rules/"
			"entry[@name='{}']"
		)

		return xpath

	@staticmethod
	def add_route():
		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/network/virtual-router/entry[@name='%s']"
			"/routing-table/ip/static-route"
		)

		element = """
			<entry name="%s">
				<destination>%s/%s</destination>
				<interface>%s</interface>
				<nexthop>
					<ip-address>%s</ip-address>
				</nexthop>
			</entry>
		"""

		return xpath, element
