#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .......API.XMLX.XMLX import XMLX
from .......PaloAltoNetworks.PaloAltoNetworks import PaloAltoNetworks
from .......Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from xml.etree.ElementTree import Element
# from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as Et


class GlobalProtectPortal(PaloAltoNetworks):
	"""
	Class to configure Global Protect Portal
	"""

	def __init__(self, panorama_ip, api_key):
		# print('++++ GlobalProtectPortal Class')
		super().__init__(panorama_ip, api_key)
		# print('---- GlobalProtectPortal Class')

	def __str__(self):
		return self.__class__.__name__

	@staticmethod
	def __xcode():
		"""
		Method to return Global Protect Portal xpath to place in API request string

		:return: xpath (XML code)
		:rtype: str
		"""

		xpath = (
			"/config/devices/entry[@name='localhost.localdomain']/template/entry[@name='%s']"
			"/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/global-protect"
			"/global-protect-portal"
		)

		return xpath

	def configure_global_protect_portal(
		self, template_name, portal_name=None, auth_profile=None, collect_hip=None, fqdn='gpcloudservice.com',
		hostname=None
	):
		xmx = XMLX()
		xpath = self.__xcode()

		# Portal Config

		element_root = Element('entry')
		element_root.set('name', '%s' % portal_name)

		x_portal_config = Element('portal-config')
		# x_local_address = Element('local-address')
		#
		# x_interface = Element('interface')
		# x_interface.text = '-'
		#
		# x_ip = Element('ip')
		#
		# x_local_address.append(x_interface)
		# x_local_address.append(x_ip)
		#
		# x_portal_config.append(x_local_address)

		# x_tls_service_profile = Element('ssl-tls-service-profile')
		# x_tls_service_profile.text = '-'
		#
		# x_portal_config.append(x_tls_service_profile)

		x_client_auth = Element('client-auth')

		x_client_entry = Element('entry')
		x_client_entry.set('name', 'DEFAULT')

		x_user_cred = Element('user-credential-or-client-cert-required')
		x_user_cred.text = 'yes'
		x_client_entry.append(x_user_cred)

		x_os = Element('os')
		x_os.text = 'Any'
		x_client_entry.append(x_os)

		x_auth_profile = Element('authentication-profile')
		x_auth_profile.text = auth_profile
		x_client_entry.append(x_auth_profile)

		x_auth_message = Element('authentication-message')
		x_auth_message.text = 'Enter login credentials'
		x_client_entry.append(x_auth_message)

		x_user_label = Element('username-label')
		x_user_label.text = 'Username'
		x_client_entry.append(x_user_label)

		x_pass_label = Element('password-label')
		x_pass_label.text = 'Password'
		x_client_entry.append(x_pass_label)

		x_client_auth.append(x_client_entry)

		x_portal_config.append(x_client_auth)

		x_login_page = Element('custom-login-page')
		x_login_page.text = 'factory-default'
		x_portal_config.append(x_login_page)

		x_home_page = Element('custom-home-page')
		x_home_page.text = 'factory-default'
		x_portal_config.append(x_home_page)

		element_root.append(x_portal_config)

		# Client Config

		x_client_config = Element('client-config')

		x_configs = Element('configs')

		x_client_config_entry = Element('entry')
		x_client_config_entry.set('name', 'DEFAULT')

		# HIP Collection

		x_hip_collection = Element('hip-collection')

		x_max_wait_time = Element('max-wait-time')
		x_max_wait_time.text = '20'
		x_hip_collection.append(x_max_wait_time)

		x_collect_hip_data = Element('collect-hip-data')
		x_collect_hip_data.text = collect_hip
		x_hip_collection.append(x_collect_hip_data)

		x_client_config_entry.append(x_hip_collection)

		# Gateways

		x_gateways = Element('gateways')
		x_external = Element('external')
		x_list = Element('list')

		x_external_gateway_entry = Element('entry')
		x_external_gateway_entry.set('name', 'GP cloud service')

		x_fqdn = Element('fqdn')
		x_fqdn.text = fqdn
		x_external_gateway_entry.append(x_fqdn)

		x_priority_rule = Element('priority-rule')
		x_priority_entry = Element('entry')
		x_priority_entry.set('name', 'Any')

		x_priority = Element('priority')
		x_priority.text = '1'
		x_priority_entry.append(x_priority)

		x_priority_rule.append(x_priority_entry)

		x_external_gateway_entry.append(x_priority_rule)

		x_manual = Element('manual')
		x_manual.text = 'yes'

		x_external_gateway_entry.append(x_manual)

		x_list.append(x_external_gateway_entry)

		x_external.append(x_list)

		x_cutoff_time = Element('cutoff-time')
		x_cutoff_time.text = '5'
		x_external.append(x_cutoff_time)

		x_gateways.append(x_external)

		x_client_config_entry.append(x_gateways)

		# Authentication Override

		x_auth_override = Element('authentication-override')

		x_accept_cookie = Element('accept-cookie')

		x_cookie_lifetime = Element('cookie-lifetime')

		x_lifetime_hours = Element('lifetime-in-hours')
		x_lifetime_hours.text = '24'

		x_cookie_lifetime.append(x_lifetime_hours)
		x_accept_cookie.append(x_cookie_lifetime)
		x_auth_override.append(x_accept_cookie)

		x_cookie_cert = Element('cookie-encrypt-decrypt-cert')
		x_cookie_cert.text = 'Authentication Cookie Cert'
		x_auth_override.append(x_cookie_cert)

		x_generate_cookie = Element('generate-cookie')
		x_generate_cookie.text = 'yes'
		x_auth_override.append(x_generate_cookie)

		x_client_config_entry.append(x_auth_override)

		# Source User

		x_source_user = Element('source-user')
		x_source_member = Element('member')
		x_source_member.text = 'any'
		x_source_user.append(x_source_member)

		x_client_config_entry.append(x_source_user)

		# OS

		x_os_user = Element('os')
		x_os_member = Element('member')
		x_os_member.text = 'any'
		x_os_user.append(x_os_member)

		x_client_config_entry.append(x_os_user)

		# Agent UI

		x_agent_ui = Element('agent-ui')

		x_agent_user_override = Element('max-agent-user-overrides')
		x_agent_user_override.text = '0'
		x_agent_ui.append(x_agent_user_override)

		x_agent_user_override_timeout = Element('agent-user-override-timeout')
		x_agent_user_override_timeout.text = '0'
		x_agent_ui.append(x_agent_user_override_timeout)

		x_client_config_entry.append(x_agent_ui)

		# GP App Config

		# x_app_config = app_config
		# x_client_config_entry.append(x_app_config)

		# Save User Credentials

		x_save_user_credential = Element('save-user-credentials')
		x_save_user_credential.text = '1'
		x_client_config_entry.append(x_save_user_credential)

		# Portal 2FA

		x_portal_2fa = Element('portal-2fa')
		x_portal_2fa.text = 'no'
		x_client_config_entry.append(x_portal_2fa)

		# Manual Gateway 2FA

		x_manual_gateway_2fa = Element('manual-only-gateway-2fa')
		x_manual_gateway_2fa.text = 'no'
		x_client_config_entry.append(x_manual_gateway_2fa)

		# Internal Gateway 2FA

		x_internal_gateway_2fa = Element('internal-gateway-2fa')
		x_internal_gateway_2fa.text = 'no'
		x_client_config_entry.append(x_internal_gateway_2fa)

		# Auto Discovery 2FA

		x_auto_discovery_2fa = Element('auto-discovery-external-gateway-2fa')
		x_auto_discovery_2fa.text = 'no'
		x_client_config_entry.append(x_auto_discovery_2fa)

		# MDM Enrollment

		x_mdm_enrollment = Element('mdm-enrollment-port')
		x_mdm_enrollment.text = '443'
		x_client_config_entry.append(x_mdm_enrollment)

		x_configs.append(x_client_config_entry)

		x_client_config.append(x_configs)

		# Agent User Override Key

		x_agent_override_key = Element('agent-user-override-key')
		x_agent_override_key.text = '6789'
		x_client_config.append(x_agent_override_key)

		element_root.append(x_client_config)

		# Clientless VPN

		x_clientless_vpn = Element('clientless-vpn')
		x_hostname = Element('hostname')
		x_hostname.text = hostname
		x_clientless_vpn.append(x_hostname)

		# x_dns_proxy = Element('dns-proxy')
		# x_dns_proxy.text = 'CloudDefault'
		# x_clientless_vpn.append(x_dns_proxy)

		x_login_lifetime = Element('login-lifetime')
		x_hours = Element('hours')
		x_hours.text = '3'
		x_login_lifetime.append(x_hours)
		x_clientless_vpn.append(x_login_lifetime)

		x_inactivity_logout = Element('inactivity-logout')
		x_minutes = Element('minutes')
		x_minutes.text = '30'
		x_inactivity_logout.append(x_minutes)
		x_clientless_vpn.append(x_inactivity_logout)

		element_root.append(x_clientless_vpn)

		# Satellite Config

		x_satellite_config = Element('satellite-config')
		x_client_cert = Element('client-certificate')
		x_local = Element('local')
		x_client_cert.append(x_local)
		x_satellite_config.append(x_client_cert)

		element_root.append(x_satellite_config)

		element = Et.tostring(element_root).decode('UTF-8')
		# print(element)
		# exit()

		try:
			uri = xmx.configure.format(self.panorama_ip, xpath % template_name, element, self.api_key)
		except Exception as e:
			NLogger.network.info('{} - Global Protect Portal: {} - {}'.format(template_name, portal_name, e))
		else:
			xmx.exec_xml_get(uri, NLogger.network, 'Global Protect Portal', portal_name)
