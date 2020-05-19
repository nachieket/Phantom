#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import logging

from time import sleep

from ....Panorama.Operations.Operations import Operations
from ....Panorama.Panorama import Panorama
from .....MultiThreading.MultiThreading import MultiThreading

from .....Logger.PoliciesLogger.PoliciesLogger import PoliciesLogger as PLogger

from .....Logger.NetworkLogger.NetworkLogger import NetworkLogger as NLogger
from .....Logger.DeviceLogger.DeviceLogger import DeviceLogger as DLogger

from .....Logger.SettingsLogger.SettingsLogger import SettingsLogger as SLogger
from .....Logger.PanoramaGenericLogger.PanoramaGenericLogger import PanoramaGenericLogger as PanLogger


class ConfigPrismaAccess(object):
	"""
	Prisma Access Playbook Class
	"""

	def __init__(self):
		super().__init__()

		self.module_dir = './azure-live/modules/PaloAltoNetworks/Panorama'
		# self.stage_dir = './playbooks/prisma-access/stage'

		self.prisma_access = logging.getLogger(__name__)
		self.prisma_access.setLevel(logging.INFO)

		self.prisma_access_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

		self.prisma_access_handler = logging.FileHandler('./playbooks/prisma-access/stage/prisma_access.log')
		self.prisma_access_handler.setFormatter(self.prisma_access_formatter)

		self.prisma_access.addHandler(self.prisma_access_handler)

	@staticmethod
	def get_panorama_status(public_ip):
		"""
		The method to get Panorama status - up or down.

		:param public_ip: Panorama public ip
		:type public_ip: str
		:return: status
		:rtype: str
		"""

		thread = MultiThreading()
		ops = Operations()

		status = ops.get_panorama_status(public_ip)

		if status == 'up':
			print('Panorama is up.')

			return status
		else:
			while status != 'up':
				print('\nPanorama is not up yet. Please investigate.')

				status = input('\nPress enter once Panorama is up. Or enter \'break\' to exit status check: ')

				if status == 'break':
					return 'down'

				status = thread.multithread(ops.get_panorama_status, 1, 1, public_ip)
				sleep(15)

	@staticmethod
	def get_panorama_api_key(public_ip, username, password):
		thread = MultiThreading()
		ops = Operations()

		count = 0

		print('Retrieving Panorama API Key.\n')

		while count < 10:
			panorama_api_key = thread.multithread(
				ops.get_api_key, 1, 1, public_ip, password, username
			)

			if panorama_api_key == 'no_key':
				print('\nPanorama key retrieval failed. Trying again.')
				count += 1
			else:
				return panorama_api_key

		panorama_api_key = input('\nRetrieve API Key manually and enter it here: ')
		return panorama_api_key

	@staticmethod
	def restart_panorama(panorama_ip, api_key):
		"""
		Method to restart Panorama

		:param panorama_ip: Panorama IP address
		:type panorama_ip: str
		:param api_key: Panorama API Key
		:type api_key: str
		:return: Panorama Status
		:rtype: str
		"""
		thread = MultiThreading()
		ops = Operations()

		restart_count = 0

		try:
			while restart_count < 5:
				print('Restarting Panorama.\n')

				result = thread.multithread(ops.request_panorama_software_restart, 1, 1, panorama_ip, api_key)

				if result == 'success':
					status = ops.get_panorama_status(panorama_ip=panorama_ip)

					print('Panorama is up\n')

					return status
				else:
					print('Panorama could not be restarted. Trying again.')

					restart_count += 1
			else:
				print('Panorama could not be restarted.\n')

				input('Press enter after manually restarting Panorama.\n')

				status = ops.get_panorama_status(panorama_ip=panorama_ip)

				return status
		except Exception as e:
			PanLogger.panorama.info('Panorama restart exception - {}'.format(e))

			print('Panorama could not be restarted.\n')

			input('Press enter after manually restarting Panorama.\n')

			status = ops.get_panorama_status(panorama_ip=panorama_ip)

			return status

	def deploy_panorama(self, parameters):
		api_key = ''
		system_version = '9.0.6'

		thread = MultiThreading()
		ops = Operations()

		panorama_ip = parameters['Panorama']['panorama_ip']

		##########################
		# Check if Panorama is up
		##########################

		print('\nChecking Panorama status.\n')

		status = self.get_panorama_status(public_ip=panorama_ip)

		if status == 'up':
			# Get Panorama API Key

			print('\nGetting Panorama API key.\n')

			api_key = self.get_panorama_api_key(
				public_ip=panorama_ip, username=parameters['Panorama']['panorama_username'],
				password=parameters['Panorama']['panorama_password']
			)

			print('Panorama API Key is: {}\n'.format(api_key))

			print('Received Panorama API key.\n')
		else:
			print('\nPanorama is not up. Existing the Playbook.\n')
			exit()

		###########################################
		# Check and Download Cloud Services Plugin
		###########################################

		plugin_download_count = 0

		if system_version == '9.0.6':
			while plugin_download_count < 5:
				print('Checking plugins in Panorama.\n')

				status = thread.multithread(ops.request_plugins_check, 1, 1, panorama_ip, api_key)

				if status == 'success':
					print('Downloading cloud services plugin on Panorama.\n')

					plugin_download_job_id = thread.multithread(
						ops.request_plugins_download_file, 1, 1, panorama_ip, api_key, 'cloud_services-1.5.0')

					print('Checking cloud services plugin download status.\n')

					result, details = thread.multithread(
						ops.request_panorama_job_status, 1, 1, panorama_ip, api_key, plugin_download_job_id
					)

					if (result == 'OK') or (result == 'FAIL' and details[0] == 'Image exists already'):
						print('Cloud services plugin downloaded.\n')

						break
					else:
						print('Cloud Serviced plugin could not be downloaded. Trying again.\n')

						plugin_download_count += 1
			else:
				print('Cloud plugin could not be downloaded.\n')

				print('Download cloud services Plugin 1.5.0 manually.\n')

				check = input('Press enter to continue or \'exit\' to exit the program.')

				if check == 'exit':
					print('Exiting the program\n')
					exit()

		################################
		# Install Cloud Services Plugin
		################################

		plugin_install_count = 0

		while plugin_install_count < 5:
			print('Installing cloud services plugin.\n')

			plugin_install_job_id = thread.multithread(
				ops.request_plugins_install, 1, 1, panorama_ip, api_key, 'cloud_services-1.5.0'
			)

			# Cloud Services Plugin Install Status

			print('Checking cloud services plugin installation status.\n')

			result, details = thread.multithread(
				ops.request_panorama_job_status, 1, 1, panorama_ip, api_key, plugin_install_job_id
			)

			if result == 'OK':
				print('Cloud services plugin installed.\n')

				print('Deployment complete\n')

				return 'complete', panorama_ip, api_key
			else:
				print('Cloud services plugin installation failed. Trying again.\n')

				plugin_install_count += 1
		else:
			print('Cloud services plugin could not be installed.\n')

			print('Install cloud services plugin manually.\n')

			check = input('Press enter to continue or enter \'exit\' to exit the program: ')

			if check == 'exit':
				print('Exiting the program.\n')
				exit()
			else:
				print('Panorama Deployment complete.\n')

				return 'complete', panorama_ip, api_key

	@staticmethod
	def configure_setup_services(panorama_ip, api_key):
		"""
		Method to configure Panorama > Setup > Services

		:param panorama_ip: panorama ip address
		:type panorama_ip: str
		:param api_key: panorama api key
		:type api_key: str
		:return: 'success' or 'failure'
		:rtype: str
		"""

		ops = Operations()

		##################
		# Panorama object
		##################

		panw = Panorama(panorama_ip=panorama_ip, api_key=api_key)

		#####################################################
		# Configure Panorama > Setup > Services: DNS and NTP
		#####################################################

		dns = {'primary': '8.8.8.8', 'secondary': '4.2.2.2'}
		ntp = {'primary': 'time.google.com', 'secondary': 'time2.google.com'}

		panw.configure_setup_services(action='add', dns=dns, ntp=ntp)

		sleep(1)

		#########
		# Commit
		#########

		try:
			catch = ops.request_panorama_commit(panorama_ip=panorama_ip, api_key=api_key)
		except Exception as e:
			PanLogger.panorama.info('Panorama > Setup > Services commit error - {}\n'.format(e))
		else:
			if catch != 'success':
				print('Panorama > Setup > Services commit error. Exiting the program.\n')
				exit()

		answer = 'no'

		while answer.lower() != 'done':
			answer = input('\nComplete cloud service plugin verification and enter \'Done\': ')

	@staticmethod
	def configure_cloud_service_infrastructure(panorama_ip, api_key, parameters):
		"""
		Method to configure Cloud Service plugin infrastructure settings

		:param panorama_ip: panorama ip address
		:type panorama_ip: str
		:param api_key: panorama api key
		:type api_key: str
		:param parameters: dictionary of all input items
		:type parameters: dict
		:return: 'success' or 'failure'
		:rtype: str
		"""

		ops = Operations()

		##################
		# Panorama object
		##################

		panw = Panorama(panorama_ip=panorama_ip, api_key=api_key)

		#####################################
		# Cloud Service Infrastructure Setup
		#####################################

		###############
		# Device Group
		###############

		panw.add_device_group(device_group='Service_Conn_Device_Group')

		sleep(1)

		###########
		# Template
		###########

		panw.add_template(template='Service_Conn_Template')

		sleep(1)

		#################
		# Template Stack
		#################

		panw.add_template_stack(template_stack='Service_Conn_Template_Stack')

		sleep(1)

		panw.add_template_to_template_stack(
			template_stack='Service_Conn_Template_Stack', templates=['Service_Conn_Template']
		)

		sleep(1)

		#######################
		# Cloud Services Setup
		#######################

		setup = parameters['Service_Connection_Setup']
		domains = {}
		count = 1

		for dom in setup.keys():
			if ('domain' + str(count)) in dom:
				domains[dom] = {}
				domains[dom]['name'] = setup[dom]

				for dns in setup.keys():
					if ('dns_servers' + str(count)) in dns:
						if type(setup[dns]) is list:
							domains[dom]['primary'] = setup[dns][0]
							domains[dom]['secondary'] = setup[dns][1]

							count += 1
							break
						else:
							domains[dom]['primary'] = setup[dns]

							count += 1
							break

		panw.configure_cloud_service_setup(
			action='add', service_subnet=setup['infrastructure_subnet'], domains=domains,
			data_lake=setup['data_lake_region']
		)

		sleep(1)

		#########
		# Commit
		#########

		try:
			catch = ops.request_panorama_commit(panorama_ip=panorama_ip, api_key=api_key)
		except Exception as e:
			PanLogger.panorama.info('Cloud services plugin infrastructure setup commit error - {}\n'.format(e))
		else:
			if catch != 'success':
				print('Cloud services plugin infrastructure setup commit error. Exiting the program.\n')
				exit()

	def configure_service_connection(self, panorama_ip, api_key, parameters):
		"""

		:param panorama_ip: panorama ip address
		:type panorama_ip: str
		:param api_key: panorama api key
		:type api_key: str
		:param parameters: dictionary of all input items
		:type parameters: dict
		:return:
		:rtype:
		"""

		ops = Operations()
		panw = Panorama(panorama_ip=panorama_ip, api_key=api_key)

		service_template = 'Service_Conn_Template'

		###############################
		# Cloud Service Infrastructure
		###############################

		try:
			self.configure_cloud_service_infrastructure(
				panorama_ip=panorama_ip, api_key=api_key, parameters=parameters
			)
		except Exception as e:
			PanLogger.panorama.info('Cloud services infrastructure setup configuration failed - {}\n'.format(e))

		#############
		# IKE Crypto
		#############

		try:
			ike_crypto_profile_name = 'prisma_access_ike_crypto'
			ike_crypto_hash_ = parameters['Service_Connections']['authentication']
			ike_crypto_dh_group = parameters['Service_Connections']['dh_group']
			ike_crypto_encryption = parameters['Service_Connections']['encryption']

			panw.add_ike_crypto_profile(
				template_name=service_template, profile_name=ike_crypto_profile_name, hash_=ike_crypto_hash_,
				dh_group=ike_crypto_dh_group, encryption=ike_crypto_encryption, lifetime={'hours': '8'}
			)
		except Exception as e:
			ike_crypto_profile_name = 'default'

			NLogger.network.info('Prisma Access IKE Crypto configuration failed - {}\n'.format(e))

		###############
		# IPSec Crypto
		###############

		try:
			ipsec_crypto_profile_name = 'prisma_access_ipsec_crypto'
			ipsec_crypto_protocol = 'ESP'
			ipsec_crypto_encryption = parameters['Service_Connections']['encryption']
			ipsec_crypto_authentication = parameters['Service_Connections']['authentication']
			ipsec_crypto_dh_group = 'group5'

			panw.add_ipsec_crypto_profile(
				template_name=service_template, profile_name=ipsec_crypto_profile_name, protocol=ipsec_crypto_protocol,
				encryption=ipsec_crypto_encryption, authentication=ipsec_crypto_authentication,
				dh_group=ipsec_crypto_dh_group, lifetime={'hours': '8'}
			)
		except Exception as e:
			ipsec_crypto_profile_name = 'default'

			NLogger.network.info('Prisma Access IPSec Crypto configuration failed - {}\n'.format(e))

		###############
		# IKE Gateway
		###############

		service_conn_gw = 'service_connection_gw'
		gw_interface = 'vlan'
		gw_peer_ip = parameters['Service_Connections']['peer_ip']
		gw_secret = parameters['Service_Connections']['ipsec_secret']

		try:
			gw_general = {
				'name': service_conn_gw, 'interface': gw_interface, 'peer_ip_address_type': 'ip',
				'peer_address': gw_peer_ip, 'authentication': 'pre-shared-key', 'pre_shared_key': gw_secret
			}

			gw_advanced_options = {
				'ikev2_dpd_interval': '10', 'ikev2_ike_crypto_profile': ike_crypto_profile_name,
				'version': 'ikev2-preferred'
			}

			panw.add_ike_gateway(template_name=service_template, general=gw_general, advanced_options=gw_advanced_options)
		except Exception as e:
			NLogger.network.info('Prisma Access IKE Gateway configuration failed - {}\n'.format(e))

			print('Exiting the program.\n')
			exit()

		###############
		# IPSec Tunnel
		###############

		ipsec_tunnel_name = 'service_connection_tunnel'

		ipsec_general = {
			'tunnel_name': ipsec_tunnel_name, 'key_type': 'auto-key', 'tunnel_interface': 'tunnel',
			'ike_gateway_name': service_conn_gw,
			'ipsec_crypto_profile': ipsec_crypto_profile_name,  'enable_replay_protection': 'yes',
			'enable_tunnel_monitor': 'yes', 'tunnel_monitor_destination_ip': '192.168.10.101'
		}

		try:
			panw.add_ipsec_tunnel(template_name=service_template, general=ipsec_general)
		except Exception as e:
			NLogger.network.info('Prisma Access IPSec tunnel configuration failed - {}\n'.format(e))

			print('Exiting the program.\n')
			exit()

		#####################
		# Service Connection
		#####################

		try:
			corporate_subnets = []

			if type(parameters['Service_Connections']['corporate_subnets']) is str:
				corporate_subnets.append(parameters['Service_Connections']['corporate_subnets'])
			elif type(parameters['Service_Connections']['corporate_subnets']) is list:
				corporate_subnets = parameters['Service_Connections']['corporate_subnets']

			region = parameters['Service_Connections']['location']

			service_connection_parameters = {
				'name': 'Primary-Service-Connection', 'subnets': corporate_subnets, 'region': region,
				'primary_ipsec_tunnel': ipsec_tunnel_name
			}

			panw.configure_service_connection(action='add', service_connection=service_connection_parameters)
		except Exception as e:
			PanLogger.panorama.info('Service connection configuration failed - {}'.format(e))

		#########
		# Commit
		#########

		try:
			catch = ops.request_panorama_commit(panorama_ip=panorama_ip, api_key=api_key)
		except Exception as e:
			PanLogger.panorama.info('Service connection commit error - {}\n'.format(e))

			print('Exiting the program.\n')
			exit()
		else:
			if catch != 'success':
				print('Service connection commit error. Exiting the program.\n')
				exit()

	@staticmethod
	def configure_mobile_user_infrastructure(panorama_ip, api_key):
		"""
		Method to configure Mobile User Infrastructure settings

		:param panorama_ip: panorama ip address
		:type panorama_ip: str
		:param api_key: panorama api key
		:type api_key: str
		:return: 'success' or 'failure'
		:rtype: str
		"""

		ops = Operations()

		##################
		# Panorama object
		##################

		panw = Panorama(panorama_ip=panorama_ip, api_key=api_key)

		###################################
		# Mobile User Infrastructure Setup
		###################################

		###############
		# Device Group
		###############

		panw.add_device_group(device_group='Mobile_User_Device_Group')

		sleep(1)

		###########
		# Template
		###########

		panw.add_template(template='Mobile_User_Template')

		sleep(1)

		#################
		# Template Stack
		#################

		panw.add_template_stack(template_stack='Mobile_User_Template_Stack')

		sleep(1)

		panw.add_template_to_template_stack(
			template_stack='Mobile_User_Template_Stack', templates=['Mobile_User_Template']
		)

		sleep(1)

		#############################
		# Mobile User Template Zones
		#############################

		panw.configure_zone(action='add', template_name='Mobile_User_Template', zone_name='Trust')
		panw.configure_zone(action='add', template_name='Mobile_User_Template', zone_name='Untrust')

		sleep(1)

		############################
		# Mobile User Trusted Zones
		############################

		panw.configure_mobile_users_trusted_zones(action='add', trusted_zones=['Trust'])

		sleep(1)

		#########
		# Commit
		#########

		try:
			catch = ops.request_panorama_commit(panorama_ip=panorama_ip, api_key=api_key)
		except Exception as e:
			PanLogger.panorama.info('Cloud services plugin mobile infrastructure setup commit error - {}\n'.format(e))
		else:
			if catch != 'success':
				print('Cloud services plugin mobile infrastructure setup commit error. Exiting the program.\n')
				exit()

	@staticmethod
	def configure_mobile_user_authentication(panorama_ip, api_key, template, parameters):
		"""
		Method to configure authentication settings under a template' Mobile User in this playbook

		:param panorama_ip: panorama ip address
		:type panorama_ip: str
		:param api_key: panorama api key
		:type api_key: str
		:param template: Panorama template name
		:type template: str
		:param parameters: dictionary of all input items
		:type parameters: dict
		:return: 'success' or 'failure'
		:rtype: str
		"""

		ops = Operations()

		##################
		# Panorama object
		##################

		panw = Panorama(panorama_ip=panorama_ip, api_key=api_key)

		################################
		# Authentication - LDAP Profile
		################################

		authentication = parameters['Authentication']

		if authentication.get('auth_type') == 'active-directory':
			auth_servers = []
			db_servers = authentication['db_servers']

			for db in db_servers:
				server = db.split(',')

				auth_servers.append(
					{
						'name': server[0],
						'address': server[1],
						'port': server[2]
					}
				)

			ldap_type = authentication.get('auth_type')
			base_dn = authentication.get('base_dn', 'dc=acme,dc=com')
			bind_dn = authentication.get('bind_dn', 'admin@acme.com')
			bind_password = authentication.get('bind_password', 'q1w2e3r4t5')

			ldap_profile_name = 'LDAP_Auth'

			panw.configure_template_ldap_profile(
				action='add', template_name=template, profile_name=ldap_profile_name,
				location='shared', auth_servers=auth_servers, ldap_type=ldap_type, base_dn=base_dn,
				bind_dn=bind_dn, bind_timelimit='30', bind_password=bind_password
			)

			sleep(1)

			##########################################
			# Authentication - Authentication Profile
			##########################################

			auth_profile_name = 'LDAP_Auth_Profile'

			panw.configure_template_authentication_profile(
				action='add', template_name=template, profile_name=auth_profile_name, location='shared',
				server_profile_name=ldap_profile_name, login_attribute='sAMAccountName', member_list=['all'],
				username_modifier='%USERINPUT%', enable_mfa='no'
			)

			sleep(1)

			################
			# User ID Agent
			################

			agents = authentication.get('user_id_agent_address')

			if type(agents) is str:
				user_id_agent_name = 'LDAP_User_ID_Agent'

				panw.configure_template_user_id_agent(
					action='add', template_name=template, agent_name=user_id_agent_name,
					agent_address=agents, agent_port='5007',
					enable_ntlm_auth='yes', enable_hip_collection='yes'
				)

				sleep(1)
			elif type(agents) is list:
				count = 1

				for agent in agents:
					user_id_agent_name = 'LDAP_User_ID_Agent' + str(count)

					panw.configure_template_user_id_agent(
						action='add', template_name=template, agent_name=user_id_agent_name,
						agent_address=agent, agent_port='5007',
						enable_ntlm_auth='yes', enable_hip_collection='yes'
					)

					count += 1

					sleep(1)

			################
			# Group Mapping
			################

			panw.configure_template_group_mapping_settings(
				action='add', template_name=template, server_profile=ldap_profile_name,
				group_mapping_name='LDAP_Group_Map', group_include_list=authentication.get('db_group_base_dn')
			)

			sleep(1)

			#########
			# Commit
			#########

			try:
				catch = ops.request_panorama_commit(panorama_ip=panorama_ip, api_key=api_key)
			except Exception as e:
				PanLogger.panorama.info(
					'Mobile user authentication configuration commit error - {}\n'.format(e))
			else:
				if catch != 'success':
					print('Mobile user authentication configuration commit error. Exiting the program.\n')
					exit()
				else:
					return auth_profile_name

	@staticmethod
	def configure_mobile_user_portal(panorama_ip, api_key, auth_profile, parameters):
		"""
		Method to configure authentication settings under a template' Mobile User in this playbook

		:param panorama_ip: panorama ip address
		:type panorama_ip: str
		:param api_key: panorama api key
		:type api_key: str
		:param auth_profile:
		:type auth_profile:
		:param parameters: dictionary of all input items
		:type parameters: dict
		:return: 'success' or 'failure'
		:rtype: str
		"""

		emea_global_regions = [
			'eu-west-2', 'belgium', 'netherlands-south', 'eu-west-3', 'andorra', 'austria', 'belarus', 'bulgaria',
			'croatia', 'czech-republic', 'denmark', 'finland', 'france-south', 'eu-central-1', 'germany-north',
			'germany-south', 'greece', 'hungary', 'eu-west-1', 'italy', 'liechtenstein', 'lithuania',
			'luxembourg', 'moldova', 'monaco', 'netherlands-central', 'norway', 'poland', 'portugal', 'romania',
			'russia-central', 'russia-northwest', 'slovakia', 'slovenia', 'spain-central', 'spain-east', 'sweden',
			'switzerland', 'ukraine', 'uzbekistan', 'kenya', 'nigeria', 'south-africa-central', 'south-africa-west',
			'me-south-1', 'egypt', 'israel', 'jordan', 'kuwait', 'saudi-arabia', 'turkey', 'uae'
		]

		amer_global_regions = [
			'canada-central', 'ca-central-1', 'canada-west', 'costa-rica', 'mexico-central', 'mexico-west',
			'panama', 'us-east-2', 'us-east-1', 'us-northeast', 'us-west-2', 'us-south', 'us-southeast',
			'us-west-201', 'us-west-1', 'argentina', 'bolivia', 'brazil-central', 'brazil-east', 'sa-east-1',
			'chile', 'columbia', 'ecuador', 'paraguay', 'peru', 'venezuela'
		]

		apac_global_regions = [
			'bangladesh', 'cambodia', 'hong-kong', 'india-north', 'india-south', 'ap-south-1', 'indonesia',
			'malaysia', 'myanmar', 'pakistan-south', 'pakistan-west', 'papua-new-guinea', 'philippines',
			'ap-southeast-1', 'ap-northeast-2', 'taiwan', 'thailand', 'vietnam', 'ap-northeast-1',
			'japan-south', 'australia-east', 'australia-south', 'ap-southeast-2', 'new-zealand'
		]

		##################
		# Panorama object
		##################

		panw = Panorama(panorama_ip=panorama_ip, api_key=api_key)

		#####################
		# Mobile User Portal
		#####################

		portal_name = parameters.get('Mobile_User_Portal')['portal_name']

		# IP Pools

		emea_ip_pools = None

		if parameters.get('Mobile_User_Portal')['emea_ip_pool'] is not None:
			if type(parameters['Mobile_User_Portal']['emea_ip_pool']) is str:
				emea_ip_pools = [(parameters['Mobile_User_Portal']['emea_ip_pool'])]
			elif type(parameters['Mobile_User_Portal']['emea_ip_pool']) is list:
				emea_ip_pools = parameters['Mobile_User_Portal']['emea_ip_pool']

		amer_ip_pools = None

		if parameters.get('Mobile_User_Portal')['amer_ip_pool'] is not None:
			if type(parameters['Mobile_User_Portal']['amer_ip_pool']) is str:
				amer_ip_pools = [parameters['Mobile_User_Portal']['amer_ip_pool']]
			elif type(parameters['Mobile_User_Portal']['amer_ip_pool']) is list:
				amer_ip_pools = parameters['Mobile_User_Portal']['amer_ip_pool']

		apac_ip_pools = None

		if parameters.get('Mobile_User_Portal')['apac_ip_pool'] is not None:
			if type(parameters['Mobile_User_Portal']['apac_ip_pool']) is str:
				apac_ip_pools = [parameters['Mobile_User_Portal']['apac_ip_pool']]
			elif type(parameters['Mobile_User_Portal']['apac_ip_pool']) is list:
				apac_ip_pools = parameters['Mobile_User_Portal']['apac_ip_pool']

		world_ip_pools = None

		if parameters.get('Mobile_User_Portal')['world_ip_pool'] is not None:
			if type(parameters['Mobile_User_Portal']['world_ip_pool']) is str:
				world_ip_pools = [parameters['Mobile_User_Portal']['world_ip_pool']]
			elif type(parameters['Mobile_User_Portal']['world_ip_pool']) is list:
				world_ip_pools = parameters['Mobile_User_Portal']['world_ip_pool']

		# DNS Domains

		if parameters.get('Mobile_User_Portal')['emea_domains'] is not None:
			emea_domains = parameters.get('Mobile_User_Portal')['emea_domains']
		else:
			emea_domains = None

		if parameters.get('Mobile_User_Portal')['amer_domains'] is not None:
			amer_domains = parameters.get('Mobile_User_Portal')['amer_domains']
		else:
			amer_domains = None

		if parameters.get('Mobile_User_Portal')['apac_domains'] is not None:
			apac_domains = parameters.get('Mobile_User_Portal')['apac_domains']
		else:
			apac_domains = None

		if parameters.get('Mobile_User_Portal')['world_domains'] is not None:
			world_domains = parameters.get('Mobile_User_Portal')['world_domains']
		else:
			world_domains = None

		regions = parameters.get('Mobile_User_Portal')['locations']

		emea_region = []
		amer_region = []
		apac_region = []

		for region in regions:
			if region in emea_global_regions:
				emea_region.append(region)
			elif region in amer_global_regions:
				amer_region.append(region)
			elif region in apac_global_regions:
				apac_region.append(region)
		else:
			if not emea_region:
				emea_region = None

			if not amer_region:
				amer_region = None

			if not apac_region:
				apac_region = None

		auth_profile = auth_profile

		if parameters.get('Mobile_User_Portal')['internal_host_detection'] is not None:
			internal_host_detection = parameters.get('Mobile_User_Portal')['internal_host_detection']
		else:
			internal_host_detection = None

		panw.configure_mobile_users_onboard(
			action='add', portal_name=portal_name, emea_ip_pools=emea_ip_pools, amer_ip_pools=amer_ip_pools,
			apac_ip_pools=apac_ip_pools, world_ip_pools=world_ip_pools, emea_domains=emea_domains,
			amer_domains=amer_domains, apac_domains=apac_domains, world_domains=world_domains,
			auth_profile=auth_profile, emea_region=emea_region, amer_region=amer_region, apac_region=apac_region,
			internal_host_detection=internal_host_detection
		)

		# #########
		# # Commit
		# #########
		#
		# try:
		# 	catch = ops.request_panorama_commit(panorama_ip=panorama_ip, api_key=api_key)
		# except Exception as e:
		# 	PanLogger.panorama.info(
		# 		'Mobile user portal configuration commit error - {}\n'.format(e))
		# else:
		# 	if catch != 'success':
		# 		print('Mobile user portal configuration commit error. Exiting the program.\n')
		# 		exit()

	@staticmethod
	def configure_mobile_user_security_policy(panorama_ip, api_key, parameters):
		"""
		Method to configure mobile user device group default security policies

		:param panorama_ip:
		:type panorama_ip:
		:param api_key:
		:type api_key:
		:param parameters:
		:type parameters:
		:return:
		:rtype:
		"""

		device_group = 'Mobile_User_Device_Group'

		ops = Operations()

		##################
		# Panorama Object
		##################

		panw = Panorama(panorama_ip=panorama_ip, api_key=api_key)

		#################
		# Log Forwarding
		#################

		auth_logs = {
			'name': 'Auth_Logs', 'type': 'auth', 'filter': 'All Logs', 'Desc': 'All Auth Logs', 'Panorama': 'yes'
		}

		data_logs = {
			'name': 'Data_Logs', 'type': 'data', 'filter': 'All Logs', 'Desc': 'All Data Logs', 'Panorama': 'yes'
		}

		threat_logs = {
			'name': 'Threat_Logs', 'type': 'threat', 'filter': 'All Logs', 'Desc': 'All Threat Logs', 'Panorama': 'yes'
		}

		traffic_logs = {
			'name': 'Traffic_Logs', 'type': 'traffic', 'filter': 'All Logs', 'Desc': 'All Traffic Logs',
			'Panorama': 'yes'
		}

		tunnel_logs = {
			'name': 'Tunnel_Logs', 'type': 'tunnel', 'filter': 'All Logs', 'Desc': 'All Tunnel Logs', 'Panorama': 'yes'
		}

		url_logs = {
			'name': 'URL_Logs', 'type': 'url', 'filter': 'All Logs', 'Desc': 'All URL Logs', 'Panorama': 'yes'
		}

		wildfire_logs = {
			'name': 'Wildfire_Logs', 'type': 'wildfire', 'filter': 'All Logs', 'Desc': 'All Wildfire Logs',
			'Panorama': 'yes'
		}

		log_forwarding_profile = 'Prisma_Access_Log_Forwarding'

		panw.configure_log_forwarding_profile(
			action='add', device_group=device_group, name=log_forwarding_profile, location='shared',
			description='Prisma Access Log Forwarding to Data Lake',
			log_types=[auth_logs, data_logs, threat_logs, traffic_logs, tunnel_logs, url_logs, wildfire_logs]
		)

		##################
		# Address Objects
		##################

		def format_address(addr):
			name = 'Net_' + addr[0] + '_' + addr[1]

			addr = '/'.join(addr)

			panw.configure_address(
				action='add', device_group=device_group, name=name, location='shared',
				description='Mobile User IP Range ' + addr,
				type_='ip-netmask', address_value=addr
			)

			return name

		#################################
		# Trust to Trust Security Policy
		#################################

		source_addresses = []

		if parameters.get('Mobile_User_Portal')['emea_ip_pool'] is not None:
			if type(parameters.get('Mobile_User_Portal')['emea_ip_pool']) is str:
				address = parameters.get('Mobile_User_Portal')['emea_ip_pool']

				source_addresses.append(format_address(address.split('/')))
			elif type(parameters.get('Mobile_User_Portal')['emea_ip_pool']) is list:
				for address in parameters.get('Mobile_User_Portal')['emea_ip_pool']:
					source_addresses.append(format_address(address.split('/')))

		if parameters.get('Mobile_User_Portal')['amer_ip_pool'] is not None:
			if type(parameters.get('Mobile_User_Portal')['amer_ip_pool']) is str:
				address = parameters.get('Mobile_User_Portal')['amer_ip_pool']

				source_addresses.append(format_address(address.split('/')))
			elif type(parameters.get('Mobile_User_Portal')['amer_ip_pool']) is list:
				for address in parameters.get('Mobile_User_Portal')['amer_ip_pool']:
					source_addresses.append(format_address(address.split('/')))

		if parameters.get('Mobile_User_Portal')['apac_ip_pool'] is not None:
			if type(parameters.get('Mobile_User_Portal')['apac_ip_pool']) is str:
				address = parameters.get('Mobile_User_Portal')['apac_ip_pool']

				source_addresses.append(format_address(address.split('/')))
			elif type(parameters.get('Mobile_User_Portal')['apac_ip_pool']) is list:
				for address in parameters.get('Mobile_User_Portal')['apac_ip_pool']:
					source_addresses.append(format_address(address.split('/')))

		if parameters.get('Mobile_User_Portal')['world_ip_pool'] is not None:
			if type(parameters.get('Mobile_User_Portal')['world_ip_pool']) is str:
				address = parameters.get('Mobile_User_Portal')['world_ip_pool']

				source_addresses.append(format_address(address.split('/')))
			elif type(parameters.get('Mobile_User_Portal')['world_ip_pool']) is list:
				for address in parameters.get('Mobile_User_Portal')['world_ip_pool']:
					source_addresses.append(format_address(address.split('/')))

		panw.configure_address_group(
			action='add', device_group='Mobile_User_Device_Group', name='Mobile_Users', location='shared',
			description='Prisma Access Mobile User IP Ranges', type_='static', address_group_value=source_addresses
		)

		destination_addresses = []

		if parameters.get('Service_Connections')['corporate_subnets'] is not None:
			if type(parameters.get('Service_Connections')['corporate_subnets']) is str:
				address = destination_addresses.append(parameters.get('Service_Connections')['corporate_subnets'])

				destination_addresses.append(format_address(address.split('/')))
			elif type(parameters.get('Service_Connections')['corporate_subnets']) is list:
				for address in parameters.get('Service_Connections')['corporate_subnets']:
					destination_addresses.append(format_address(address.split('/')))

		panw.configure_address_group(
			action='add', device_group='Mobile_User_Device_Group', name='Corporate_Subnets', location='shared',
			description='Prisma Access Corporate Subnet IP Ranges', type_='static',
			address_group_value=destination_addresses
		)

		panw.configure_security_rule(
			action='add', position='Pre', rule_name='Trust_to_Trust', device_group='Mobile_User_Device_Group',
			source_zone=['Trust'], source_address=['Mobile_Users'], source_user=['any'], hip_profile=['any'],
			destination_zone=['Trust'], destination_address=['Corporate_Subnets'], application=['any'],
			service=['any'], url_category=['any'], rule_action='allow', virus='default', spyware='default',
			vulnerability='default', log_forwarding=log_forwarding_profile
		)

		###################################
		# Trust to Untrust Security Policy
		###################################

		panw.configure_security_rule(
			action='add', position='Pre', rule_name='Internet', device_group='Mobile_User_Device_Group',
			source_zone=['Trust'], source_address=['Mobile_Users'], source_user=['any'], hip_profile=['any'],
			destination_zone=['Untrust'], destination_address=['any'], application=['any'], service=['any'],
			url_category=['any'], rule_action='allow', virus='default', spyware='default', vulnerability='default',
			url_filtering='default', file_blocking='basic file blocking', wildfire='default',
			log_forwarding=log_forwarding_profile
		)

		#########
		# Commit
		#########

		try:
			catch = ops.request_panorama_commit(panorama_ip=panorama_ip, api_key=api_key)
		except Exception as e:
			PanLogger.panorama.info('Mobile user security policy commit error - {}'.format(e))
		else:
			if catch == 'success':
				return 'success'
			else:
				print('Mobile user security policy commit error. Exiting the program.')
				exit()

	def configure_mobile_user(self, panorama_ip, api_key, parameters):
		"""

		:param panorama_ip: panorama ip address
		:type panorama_ip: str
		:param api_key: panorama api key
		:type api_key: str
		:param parameters: dictionary of all input items
		:type parameters: dict
		:return:
		:rtype:
		"""

		auth_profile = 'LDAP_Auth_Profile'

		#############################
		# Mobile User Infrastructure
		#############################

		try:
			self.configure_mobile_user_infrastructure(panorama_ip=panorama_ip, api_key=api_key)
		except Exception as e:
			SLogger.settings.info('Error configuring mobile user infrastructure setup - {}'.format(e))

		#################
		# Authentication
		#################

		try:
			auth_profile = self.configure_mobile_user_authentication(
				panorama_ip=panorama_ip, api_key=api_key, template='Mobile_User_Template', parameters=parameters
			)
		except Exception as e:
			DLogger.device.info('Mobile user authentication settings configuration failed - {}'.format(e))
			print('AuthProfile - Exiting the playbook.\n')
			exit()

		##############################
		# Mobile User Security Policy
		##############################

		try:
			self.configure_mobile_user_security_policy(
				panorama_ip=panorama_ip, api_key=api_key, parameters=parameters
			)
		except Exception as e:
			PLogger.policies.info('Mobile user security policies configuration failed - {}'.format(e))
			print('Security Policy - Exiting the playbook.\n')
			exit()

		#####################
		# Mobile User Portal
		#####################

		try:
			self.configure_mobile_user_portal(
				panorama_ip=panorama_ip, api_key=api_key, parameters=parameters, auth_profile=auth_profile
			)
		except Exception as e:
			SLogger.settings.info('Mobile user portal settings configuration failed - {}'.format(e))
			print('Mobile Portal - Exiting the playbook.\n')
			exit()

	def configure_panorama(self, panorama_ip, api_key, parameters):
		"""
		Method to configure Panorama

		:param panorama_ip: panorama ip address
		:type panorama_ip: str
		:param api_key: panorama api key
		:type api_key: str
		:param parameters: dictionary of all input items
		:type parameters: dict
		:return:
		:rtype:
		"""

		# ##############################
		# # Panorama > Setup > Services
		# ##############################
		#
		# try:
		# 	self.configure_setup_services(panorama_ip=panorama_ip, api_key=api_key)
		# except Exception as e:
		# 	PanLogger.panorama.info('Error configuring Panorama > Setup > Services - {}\n'.format(e))

		#########################################
		# Cloud Service Connection Configuration
		#########################################

		try:
			self.configure_service_connection(
				panorama_ip=panorama_ip, api_key=api_key, parameters=parameters
			)
		except Exception as e:
			PanLogger.panorama.info('Error configuring service connection setup - {}'.format(e))

		############################
		# Mobile User Configuration
		############################

		try:
			self.configure_mobile_user(
				panorama_ip=panorama_ip, api_key=api_key, parameters=parameters
			)
		except Exception as e:
			PanLogger.panorama.info('Error configuring mobile user setup - {}'.format(e))

	def orchestrator(self, parameters):
		"""
		Method to orchestrate Prisma Access deployment

		:param parameters: dictionary of all input items
		:type parameters: dict
		:return:
		:rtype:
		"""
		thread = MultiThreading()

		##################
		# Deploy Panorama
		##################

		status, panorama_ip, api_key = self.deploy_panorama(parameters=parameters)

		status = 'complete'

		#####################
		# Configure Panorama
		#####################

		if status == 'complete':

			##############################
			# Panorama > Setup > Services
			##############################

			print('Configuring DNS and NTP servers on Panorama. Please wait.')

			try:
				self.configure_setup_services(panorama_ip=panorama_ip, api_key=api_key)
			except Exception as e:
				PanLogger.panorama.info('Error configuring Panorama > Setup > Services - {}\n'.format(e))

			#########################
			# Panorama Configuration
			#########################

			print('\nConfiguring Panorama\n')

			thread.multithread(
				self.configure_panorama, 1, 1, panorama_ip, api_key, parameters
			)

			print('Panorama configuration finished.\n')
		else:
			print('Panorama deployment failed. Exiting the program.\n')
