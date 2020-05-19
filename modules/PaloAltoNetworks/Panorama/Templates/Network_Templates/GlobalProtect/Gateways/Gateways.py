#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class GlobalProtectGateway(PaloAltoNetworks):
	"""
	Class to configure Global Protect Gateway
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ GlobalProtectGateway Class')
		super().__init__(panorama_ip, api_key)
		# print('---- GlobalProtectGateway Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Global Protect Gateway xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/global-protect"
			"/global-protect-gateway"
		)

		return xpath

	def configure_global_protect_gateway(
		self, template_name, gateway_name=None, auth_profile=None
	):
		xmx = XMLX()
		xpath = self.__xcode()

		# Client Auth

		element_root = Element('entry')
		element_root.set('name', '%s' % gateway_name)

		x_client_auth = Element('client-auth')

		x_client_auth_entry = Element('entry')
		x_client_auth_entry.set('name', 'DEFAULT')

		x_os = Element('os')
		x_os.text = 'Any'
		x_client_auth_entry.append(x_os)

		x_auth_profile = Element('authentication-profile')
		x_auth_profile.text = auth_profile
		x_client_auth_entry.append(x_auth_profile)

		x_auth_message = Element('authentication-message')
		x_auth_message.text = 'Enter login credentials'
		x_client_auth_entry.append(x_auth_message)

		x_user_cred = Element('user-credential-or-client-cert-required')
		x_user_cred.text = 'yes'
		x_client_auth_entry.append(x_user_cred)

		x_user_label = Element('username-label')
		x_user_label.text = 'Username'
		x_client_auth_entry.append(x_user_label)

		x_pass_label = Element('password-label')
		x_pass_label.text = 'Password'
		x_client_auth_entry.append(x_pass_label)

		x_client_auth.append(x_client_auth_entry)

		element_root.append(x_client_auth)

		# Remote User Tunnel Config

		x_remote_user_tunnel = Element('remote-user-tunnel-configs')

		x_remote_user_entry = Element('entry')
		x_remote_user_entry.set('name', 'DEFAULT')

		x_split_tunnel = Element('split-tunneling')

		x_include_domains = Element('include-domains')
		x_include_list = Element('list')
		x_include_domains.append(x_include_list)
		x_split_tunnel.append(x_include_domains)

		x_exclude_domains = Element('exclude-domains')
		x_exclude_list = Element('list')
		x_exclude_domains.append(x_exclude_list)
		x_split_tunnel.append(x_exclude_domains)

		x_access_route = Element('access-route')
		x_split_tunnel.append(x_access_route)

		x_exclude_access_route = Element('exclude-access-route')
		x_split_tunnel.append(x_exclude_access_route)

		x_include_apps = Element('include-applications')
		x_split_tunnel.append(x_include_apps)

		x_exclude_apps = Element('exclude-applications')
		x_split_tunnel.append(x_exclude_apps)

		x_remote_user_entry.append(x_split_tunnel)

		# Authentication Override

		x_auth_override = Element('authentication-override')

		x_accept_cookie = Element('accept-cookie')
		x_cookie_lifetime = Element('cookie-lifetime')
		x_lifetime_hours = Element('lifetime-in-hours')
		x_lifetime_hours.text = '24'
		x_cookie_lifetime.append(x_lifetime_hours)
		x_accept_cookie.append(x_cookie_lifetime)
		x_auth_override.append(x_accept_cookie)

		x_cookie_encrypt = Element('cookie-encrypt-decrypt-cert')
		x_cookie_encrypt.text = 'Authentication Cookie Cert'
		x_auth_override.append(x_cookie_encrypt)

		x_generate_cookie = Element('generate-cookie')
		x_generate_cookie.text = 'yes'
		x_auth_override.append(x_generate_cookie)

		x_remote_user_entry.append(x_auth_override)

		# Source Address

		x_source_address = Element('source-address')
		x_ip_address = Element('ip-address')
		x_source_address.append(x_ip_address)

		x_region = Element('region')
		x_source_address.append(x_region)

		x_remote_user_entry.append(x_source_address)

		# Source User

		x_source_user = Element('source-user')
		x_source_user_member = Element('member')
		x_source_user_member.text = 'any'
		x_source_user.append(x_source_user_member)

		x_remote_user_entry.append(x_source_user)

		# Authentication Server Pool

		x_auth_server_pool = Element('authentication-server-ip-pool')
		x_remote_user_entry.append(x_auth_server_pool)

		# IP Pool

		x_ip_pool = Element('ip-pool')
		x_remote_user_entry.append(x_ip_pool)

		# OS

		x_tun_os = Element('os')
		x_tun_os_member = Element('member')
		x_tun_os_member.text = 'any'
		x_tun_os.append(x_tun_os_member)

		x_remote_user_entry.append(x_tun_os)

		# Framed IP

		x_framed_ip = Element('retrieve-framed-ip-address')
		x_framed_ip.text = 'no'
		x_remote_user_entry.append(x_framed_ip)

		# No Direct Access

		x_direct_access = Element('no-direct-access-to-local-network')
		x_direct_access.text = 'no'

		x_remote_user_entry.append(x_direct_access)

		x_remote_user_tunnel.append(x_remote_user_entry)

		element_root.append(x_remote_user_tunnel)

		# TLS Service Profile

		# x_tls_profile = Element('ssl-tls-service-profile')
		# x_tls_profile.text = '-'
		# element_root.append(x_tls_profile)

		# Tunnel Mode

		x_tunnel_mode = Element('tunnel-mode')
		x_tunnel_mode.text = 'yes'
		element_root.append(x_tunnel_mode)

		# Remote User Tunnel

		# x_remote_tunnel = Element('remote-user-tunnel')
		# x_remote_tunnel.text = '-'
		# element_root.append(x_remote_tunnel)

		# Roles

		x_roles = Element('roles')
		x_roles_entry = Element('entry')
		x_roles_entry.set('name', 'default')

		x_roles_login_lifetime = Element('login-lifetime')
		x_roles_login_lifetime_days = Element('days')
		x_roles_login_lifetime_days.text = '30'
		x_roles_login_lifetime.append(x_roles_login_lifetime_days)
		x_roles_entry.append(x_roles_login_lifetime)

		x_roles_inactivity = Element('inactivity-logout')
		x_roles_inactivity_hours = Element('hours')
		x_roles_inactivity_hours.text = '3'
		x_roles_inactivity.append(x_roles_inactivity_hours)
		x_roles_entry.append(x_roles_inactivity)

		x_roles_disconnect = Element('disconnect-on-idle')
		x_roles_disconnect_minutes = Element('minutes')
		x_roles_disconnect_minutes.text = '180'
		x_roles_disconnect.append(x_roles_disconnect_minutes)
		x_roles_entry.append(x_roles_disconnect)

		x_roles.append(x_roles_entry)

		element_root.append(x_roles)

		element = Et.tostring(element_root).decode('UTF-8')

		try:
			uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
		except Exception as e:
			NLogger.network.info('{} - Global Protect Gateway: {} - {}'.format(template_name, gateway_name, e))
		else:
			xmx.exec_xml_get(uri, NLogger.network, 'Global Protect Gateway', gateway_name)
