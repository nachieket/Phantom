#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .AWS_Provider.AWSProvider import AWSProvider
from .AWS_S3.AWSS3 import AWSS3


class AWSCloud(AWSProvider, AWSS3):
	"""
	AWS Cloud Class
	"""

	def __init__(self):
		super().__init__()
		super(AWSProvider, self).__init__()
