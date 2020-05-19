#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import argparse
from ..modules.PaloAltoNetworks.FileParser.Miscellaneous import Miscellaneous as Misc
from ..modules.Orchestrator import Orchestrate
from ..modules.PaloAltoNetworks.Panorama.Panorama import Panorama


def runtime():
	"""Function for run time parameters"""

	parser = argparse.ArgumentParser(
		usage='%(prog)s -c -f <file> OR %(prog)s -d -f <file>', description='AWS Transit Gateway'
	)

	parser.add_argument('-c', '--create', action='store_const', help='Create TGW Architecture', const='create')
	parser.add_argument('-d', '--delete', action='store_const', help='Delete TGW Architecture', const='delete')
	parser.add_argument('-f', '--file', action='store', help='TGW Architecture File', metavar='<FILE>')

	args = parser.parse_args()

	if (args.file and args.create) and args.delete is None:
		return args.file, 'create'
	elif (args.file and args.delete) and args.create is None:
		return args.file, 'delete'
	else:
		print('Incorrect set of arguments or mandatory runtime parameters are missing.')
		print('Run \'aws -h\'.')
		print('Exiting the program.')
		exit()


def main():
	"""Transit Gateway Main Method"""

	key = (
		'LUFRPT1UQWp4c2FFME96Y2FmbmgyNDQ1SktYVzJ0SU09VDN3RHg4MEUzWThrbWlHSXBQaW9BZWxGYmZSaWNHaTcxcVZiOHNQS0V5Mml'
		'4amNndlRmWDNzVVpnK212VlN6Zg=='
	)

	# xkey = (
	# 	'LUFRPT1ubEVHM3VjUUxHZktyL01LR3R4QitMUmlxbE09WnZiZGQ5VkF1a1pMRmRYNFhvcW1XYWIycUNYSFNnbzVqTHZINFFSelh4ajB'
	# 	'pWnFxUEpZcWpXSno2OUJCTnNMUw=='
	# )

	# help(Panorama)
	#
	# p = Panorama(panorama_ip='40.127.245.79', api_key=xkey)
	p = Panorama(panorama_ip='192.168.55.5', api_key=key)

	# auth = {
	# 	'name': 'Auth_Logs', 'type': 'auth', 'filter': 'All Logs', 'Desc': 'All Auth Logs', 'Panorama': 'yes',
	# 	'snmp': ['1.1.1.1'], 'email': ['someone@xyz.com'], 'syslog': ['2.2.2.2'], 'http': ['3.3.3.3']
	# }
	#
	# data = {
	# 	'name': 'Data_Logs', 'type': 'data', 'filter': 'All Logs', 'Desc': 'All Data Logs', 'Panorama': 'yes'
	# }
	#
	# threat = {
	# 	'name': 'Threat_Logs', 'type': 'threat', 'filter': 'All Logs', 'Desc': 'All Threat Logs', 'Panorama': 'yes'
	# }
	#
	# traffic = {
	# 	'name': 'Traffic_Logs', 'type': 'traffic', 'filter': 'All Logs', 'Desc': 'All Traffic Logs', 'Panorama': 'yes'
	# }
	#
	# tunnel = {
	# 	'name': 'Tunnel_Logs', 'type': 'tunnel', 'filter': 'All Logs', 'Desc': 'All Tunnel Logs', 'Panorama': 'yes'
	# }
	#
	# url = {
	# 	'name': 'URL_Logs', 'type': 'url', 'filter': 'All Logs', 'Desc': 'All URL Logs', 'Panorama': 'yes'
	# }
	#
	# wildfire = {
	# 	'name': 'Wildfire_Logs', 'type': 'wildfire', 'filter': 'All Logs', 'Desc': 'All Wildfire Logs',
	# 	'Panorama': 'yes'
	# }

	# p.configure_log_forwarding_profile(
	# 	action='add', device_group='PANW', name='GA_Log_Forwarding_Profile',
	# 	description='Prisma Access Log Forwarding Profile',
	# 	log_types=[auth, data, threat, traffic, tunnel, url, wildfire], enhanced_app_logging='yes'
	# )

	auth = {
		'name': 'Auth_Logs', 'type': 'auth', 'filter': 'All Logs', 'Desc': 'All Auth Logs', 'Panorama': 'yes'
	}

	data = {
		'name': 'Data_Logs', 'type': 'data', 'filter': 'All Logs', 'Desc': 'All Data Logs', 'Panorama': 'yes'
	}

	threat = {
		'name': 'Threat_Logs', 'type': 'threat', 'filter': 'All Logs', 'Desc': 'All Threat Logs', 'Panorama': 'yes'
	}

	traffic = {
		'name': 'Traffic_Logs', 'type': 'traffic', 'filter': 'All Logs', 'Desc': 'All Traffic Logs', 'Panorama': 'yes'
	}

	tunnel = {
		'name': 'Tunnel_Logs', 'type': 'tunnel', 'filter': 'All Logs', 'Desc': 'All Tunnel Logs', 'Panorama': 'yes'
	}

	url = {
		'name': 'URL_Logs', 'type': 'url', 'filter': 'All Logs', 'Desc': 'All URL Logs', 'Panorama': 'yes'
	}

	wildfire = {
		'name': 'Wildfire_Logs', 'type': 'wildfire', 'filter': 'All Logs', 'Desc': 'All Wildfire Logs',
		'Panorama': 'yes'
	}

	p.configure_log_forwarding_profile(
		action='add', location='shared', name='GA_Log_Forwarding_Profile',
		description='Prisma Access Log Forwarding Profile',
		log_types=[auth, data, threat, traffic, tunnel, url, wildfire], enhanced_app_logging='yes'
	)

	# p.configure_address(
	# 	action='add', device_group='PANW', name='Desktop101', description='Corporate Machine',
	# 	type_='ip-range', address_value='1.1.1.1-1.1.1.10', tag=['Critical', 'Allow']
	# )
	#
	# p.configure_address(
	# 	action='add', device_group='PANW', name='Desktop102', description='Corporate Machine',
	# 	type_='ip-wildcard', address_value='10.20.1.0/0.0.248.255'
	# )
	#
	# p.configure_address(
	# 	action='add', device_group='PANW', name='Desktop103', description='Corporate Machine',
	# 	type_='fqdn', address_value='www.msn.com', tag=['Critical', 'Allow']
	# )
	#
	# p.configure_address(
	# 	action='add', device_group='PANW', name='Desktop104', description='Corporate Machine',
	# 	type_='ip-netmask', address_value='2.2.2.0/28', tag=['Critical', 'Allow']
	# )

	# p.configure_address_group(
	# 	action='add', device_group='PANW', name='group101', description='Corporate Group',
	# 	type_='static', address_group_value=['Desktop101', 'Desktop103'], tag=['Critical', 'Allow']
	# )
	#
	# p.configure_address(
	# 	action='add', location='shared', name='Desktop111', description='Corporate Machine',
	# 	type_='ip-range', address_value='1.1.1.1-1.1.1.10', tag=['Critical', 'Allow']
	# )
	#
	# p.configure_address(
	# 		action='add', location='shared', name='Desktop112', description='Corporate Machine',
	# 		type_='fqdn', address_value='www.msn.com', tag=['Critical', 'Allow']
	# 	)
	#
	# p.configure_address_group(
	# 	action='add', location='shared', name='group102', description='Corporate Group',
	# 	type_='static', address_group_value=['Desktop111', 'Desktop112'], tag=['Allow']
	# )

	# p.configure_security_rule(
	# 	action='add', position='Pre', rule_name='rule_01', device_group='PANW', source_zone=['trust'],
	# 	source_address=['10.10.10.0/24', '172.16.10.0/24'], source_user=['any'], hip_profile=['any'],
	# 	destination_zone=['untrust'], destination_address=['1.1.1.0/24', '2.2.2.0/24'],
	# 	application=['facebook', 'ssl'], service=['application-default'], url_category=['any'], rule_action='allow',
	# 	data_filtering='something'
	# )

	# mobile_users_parameters = {
	# 	'portal_name': 'paloaltonetworks',
	# 	'ip_pools': {
	# 		'EMEA': {'pool1': '10.1.0.0/16', 'pool2': '11.1.0.0/16'},
	# 		'AMER': {'pool1': '10.2.0.0/16'},
	# 		'APAC': {'pool1': '10.3.0.0/16'},
	# 		'WORLD': {'pool1': '10.4.0.0/14'}
	# 	},
	# 	'dns': {
	# 		'EMEA': {
	# 			'domains': {'domain1': 'xyz.com', 'domain2': 'def.com'},
	# 			'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'
	# 		},
	# 		'AMER': {
	# 			'domains': {'domain1': 'abc.com'},
	# 			'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'
	# 		},
	# 		'APAC': {
	# 			'domains': {'domain1': 'qwe.com'},
	# 			'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'
	# 		},
	# 		'WORLD': {
	# 			'domains': {'domain1': 'wer.com'},
	# 			'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'
	# 		}
	# 	},
	# 	'auth_profile': 'Local_Database',
	# 	'authentication_override_cert': 'Authentication Cookie Cert',
	# 	'global_protect_portal': 'GlobalProtect_Portal',
	# 	'global_protect_gateway': 'GlobalProtect_External_Gateway',
	# 	'deployment_region': {
	# 		'EMEA': {
	# 			'loc1': 'eu-west-2', 'loc2': 'belgium', 'loc3': 'netherlands-south', 'loc4': 'eu-west-3'
	# 		},
	# 		'AMER': {
	# 			'loc1': 'us-east-1', 'loc2': 'us-east-2'
	# 		},
	# 		'APAC': {
	# 			'loc1': 'india-north', 'loc2': 'india-south'
	# 		}
	# 	},
	# 	'manual_gateway_region': {
	# 		'EMEA': {
	# 			'loc1': 'eu-west-2', 'loc2': 'belgium', 'loc3': 'netherlands-south', 'loc4': 'eu-west-3'
	# 		},
	# 		'AMER': {
	# 			'loc1': 'us-east-1', 'loc2': 'us-east-2'
	# 		},
	# 		'APAC': {
	# 			'loc1': 'india-north', 'loc2': 'india-south'
	# 		}
	# 	},
	# 	'internal_host_detection': {'ip': '10.10.10.10', 'fqdn': 'www.system.com'}
	# }
	#
	# p.configure_mobile_users(action='add', mobile_users_parameters=mobile_users_parameters)

	# mobile_users_setup_parameters = {'trusted_zones': {'zone1': 'Trust'}}
	#
	# p.configure_mobile_users_setup(action='add', mobile_users_setup=mobile_users_setup_parameters)

	# service_connection_parameters = {
	# 	'name': 'Secondary-Service-Connection', 'enable_bgp': 'yes',
	# 	'bgp': {
	# 		'peer_as': '65544', 'peer_ip': '1.1.1.1', 'local_ip': '192.168.100.1',
	# 		'advertise_prisma_access_routes': 'yes', 'secret': 'q1w2e3r4'
	# 	},
	# 	'subnets': {'subnet1': '10.10.10.0/24', 'subnet2': '172.16.10.0/24'}, 'region': 'eu-west-2',
	# 	'primary_ipsec_tunnel': 'CiscoASA-IPSec-Tunnel-Default', 'enable_secondary_wan': 'yes',
	# 	'secondary_ipsec_tunnel': 'CiscoISR-IPSec-Tunnel-Default'
	# }
	#
	# p.configure_service_connection(action='add', service_connection=service_connection_parameters)

	# service_setup_parameters = {
	# 	'service_subnet': '10.10.0.0/16', 'bgp_as': '65534',
	# 	'domains': {
	# 		'domain1': {'name': 'xyz.com', 'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'},
	# 		'domain2': {'name': 'abc.com', 'primary_dns': '8.8.8.8', 'secondary_dns': '4.2.2.2'}
	# 	},
	# 	'hip_redistribution': 'yes', 'template_stack': 'Service_Conn_Template_Stack',
	# 	'device_group': 'Service_Conn_Device_Group'
	# }
	#
	# p.configure_service_setup(action='add', service_setup=service_setup_parameters)

	# zone_parameters = {
	# 	'zone_name': 'dmz', 'zone_type': 'layer3',
	# 	'zone_protection_profile': 'default_zone_protection_profile', 'log_setting': 'Default-Logging-Profile',
	# 	'enable_packet_buffer_protection': 'yes', 'enable_user_identification': 'yes',
	# 	'user_acl': {
	# 		'include-list': {'list1': '10.10.10.0/24', 'list2': '172.16.10.0/24'},
	# 		'exclude-list': {'list1': '10.10.10.0/29', 'list2': '172.16.10.0/29'}
	# 	}
	# }
	#
	# p.configure_zone(action='add', template_name='PANW', zone=zone_parameters)
	#
	# ethernet_parameters = {
	# 	'ethernet_name': 'ethernet1/4', 'zone_name': 'dmz',
	# 	'ip_address': {'ip1': '192.168.100.1/24', 'ip2': '192.168.101.1/24'},
	# 	'enable_router_advertisement': 'yes', 'interface_management_profile': 'allow-all-int-mgmt'
	# }
	#
	# p.configure_ethernet_interface(action='add', template_name='PANW', ethernet=ethernet_parameters)
	#
	# tunnel_parameters = {
	# 	'tunnel_name': 'tunnel.21', 'zone_name': 'dmz',
	# 	'ip_address': {'ip1': '192.168.100.1/24', 'ip2': '192.168.101.1/24'},
	# 	'interface_management_profile': 'allow-all-int-mgmt'
	# }
	#
	# p.configure_tunnel_interface(action='add', template_name='PANW', tunnel=tunnel_parameters)

	# int_mgmt = {
	# 	'int_mgmt_name': 'allow-all', 'enable_https': 'yes', 'enable_ping': 'yes', 'enable_ssh': 'yes',
	# 	'enable_permitted_ip': {'ip1': '10.10.10.0/24', 'ip2': '172.16.10.0/24'}
	# }
	#
	# p.add_interface_mgmt(template_name='PANW', int_mgmt=int_mgmt)

	# p.add_template(template='Sample1')
	# p.add_template(template='Sample2')
	#
	# p.add_template_to_template_stack(template_stack='SampleStack', templates=['Sample1', 'Sample2'])
	# p.add_fw_to_template_stack(template_stack='SampleStack', firewalls=['015351000024056'])
	#
	# p.add_device_group(device_group='DGSample')
	# p.add_fw_to_device_group(device_group='DGSample', firewalls=['015351000024056'])

	# p.add_ike_crypto_profile(
	# 	template_name='PANW', profile_name='PA_Crypto', hash_=['sha1', 'sha256'], dh_group=['group2', 'group5'],
	# 	encryption=['aes-128-cbc'], lifetime={'hours': '8'}
	# )

	# p.add_ipsec_crypto_profile(
	# 	template_name='PANW', profile_name='IPSec_Crypto', protocol='ESP', encryption=['aes-128-cbc'],
	# 	authentication=['sha1'], dh_group='group20', lifetime={'hours': '8'}
	# )

	# p.add_ipsec_crypto_profile(
	# 	template_name='PANW', profile_name='IPSec_Crypto', protocol='AH',
	# 	authentication=['sha1'], dh_group='group20', lifetime={'hours': '8'}
	#

	# general = {
	# 	'tunnel_name': 'Madrid-IPSec-Tunnel', 'tunnel_interface': 'tunnel.11', 'key_type': 'auto-key',
	# 	'ike_gateway_name': 'London-GW', 'ipsec_crypto_profile': 'IPSec_Crypto', 'enable_replay_protection': 'yes',
	# 	'copy_tos_header': 'yes', 'enable_gre_encapsulation': 'yes', 'enable_tunnel_monitor': 'yes',
	# 	'tunnel_monitor_destination_ip': '172.16.10.1', 'tunnel_monitor_profile': 'default'
	# }
	#
	# proxy_ids = {
	# 	'proxy_id1': {
	# 		'proxy_id_name': 'proxy-id1', 'proxy_id_local_address': '10.10.10.0/24',
	# 		'proxy_id_remote_address': '172.16.10.0/24', 'proxy_id_protocol': {'protocol': 'any'}},
	#
	# 	'proxy_id2': {
	# 		'proxy_id_name': 'proxy-id2', 'proxy_id_local_address': '10.10.10.0/24',
	# 		'proxy_id_remote_address': '172.16.20.0/24',
	# 		'proxy_id_protocol': {'protocol': 'tcp', 'local_port': '0', 'remote_port': '8080'}}
	# }
	#
	# p.add_ipsec_tunnel(template_name='PANW', general=general, proxy_ids=proxy_ids)

	# print(p.settings_logger)
	# t = Settings(panorama_ip='192.168.55.5', api_key=key)
	#
	# t.add_template('DarkNet')

	# p.add_security_rule()

	# p.add_security_rule(
	# 	position='Pre', rule_name='rule110', device_group='PANW', source_zone='trust', source_address='10.10.10.0/24',
	# 	source_user='any', hip_profile='any', destination_zone='untrust', destination_address='1.1.1.0/24',
	# 	application='facebook', service='application-default', url_category='any', action='allow',
	# )
	#
	# p.move_security_rule('Pre', 'PANW', 'rule110', 'top')

	# p.add_snat_rule(
	# 	'192.168.55.5', key, 'Pre', 'rule103', 'PANW', 'trust', 'untrust', 'any', 'service-http', 'any',
	# 	'any', 'yes', 'dynamic-ip-and-port', '192.168.55.20', 'ethernet1/1'
	# )

	# p.add_nat_rule(
	# 	position='Pre', rule_name='rule110', device_group='PANW',
	# 	source_zone='trust', destination_zone='untrust', destination_interface='any', service='service-http',
	# 	source_address='any', destination_address='any', snat_interface_ip='192.168.55.20',
	# 	snat_interface_name='ethernet1/1'
	# )
	#
	# p.add_nat_rule(
	# 	position='Pre', rule_name='rule32', device_group='PANW',
	# 	source_zone='untrust', destination_zone='trust', destination_interface='any', service='service-http',
	# 	source_address='any', destination_address='any', snat_interface_ip='192.168.45.20',
	# 	snat_interface_name='ethernet1/2', destination_translated_address='192.168.45.150',
	# 	destination_translated_port='8080'
	# )

	# p.move_nat_rule('Pre', 'PANW', 'rule110', 'top')
	# p.move_nat_rule('Pre', 'PANW', 'rule31', 'top')

	# p.add_dnat_rule(
	# 	ip='192.168.55.5', key=key, position='Pre', rule_name='rule12', device_group='PANW', src_zone='untrust',
	# 	dst_zone='trust', dst_int='any', service='service-http', src_addr='any', dst_addr='any', snat_enable='yes',
	# 	snat_method='dynamic-ip-and-port', interface_ip='192.168.55.20', interface_name='ethernet1/1',
	# 	dnat_method='static-ip', dst_translated_addr='192.168.45.150', dst_translated_port='8080'
	# )

	exit()

	file, action = runtime()

	miscobj = Misc()
	miscobj.parse_input_file(file)

	# print(miscobj.vals)
	# print('\n' * 5)
	# print(miscobj.tgw)
	# exit()

	orchobj = Orchestrate()
	orchobj.orchestrator(miscobj.vals, action, miscobj.tgw)


if __name__ == '__main__':
	main()
