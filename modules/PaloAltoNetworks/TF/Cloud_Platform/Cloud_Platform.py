#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .AWS_Cloud.AWS_Cloud import AWSCloud


class CloudPlatform(AWSCloud):
	"""
	Cloud Platform Class
	"""

	def __init__(self):
		super().__init__()
