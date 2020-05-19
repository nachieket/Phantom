#!/usr/bin/env /Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from .Cloud_Platform.Cloud_Platform import CloudPlatform
from .TFConfigFiles.TFConfigFiles import TFConfigFiles
from .TFLogFiles.TFLogFiles import TFLogFiles
from .TFActions.TFActions import TFActions
from .PANW.Panorama_TF.AWS.AWSPanoramaTF import AWSPanoramaTF
from .PANW.Panorama_TF.Azure.AzurePanoramaTF import AzurePanoramaTF


class TF(CloudPlatform, TFConfigFiles, TFLogFiles, TFActions, AWSPanoramaTF, AzurePanoramaTF):
	"""
	Terraform Class
	"""

	def __init__(self):
		super().__init__()
		super(CloudPlatform, self).__init__()
		super(TFConfigFiles, self).__init__()
		super(TFLogFiles, self).__init__()
		super(TFActions, self).__init__()
		super(AWSPanoramaTF, self).__init__()
