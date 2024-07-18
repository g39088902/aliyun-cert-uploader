# -*- coding: utf-8 -*-
import os
import datetime
from Tea.core import TeaCore
from alibabacloud_cas20200407.client import Client as CasClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cas20200407 import models as cas_models
from alibabacloud_tea_util.client import Client as UtilClient

"""
createClient  创建客户端
"""
config = open_api_models.Config()
# 您账号所属的AccessKey ID
config.access_key_id = os.getenv('ACCESS_KEY_ID')
# 您账号所属的AccessKey Secret
config.access_key_secret = os.getenv('ACCESS_KEY_SECRET')
config.endpoint = 'cas.aliyuncs.com'
client = CasClient(config)


request = cas_models.UploadUserCertificateRequest()
today = datetime.date.today()
request.name = today.strftime("%Y.%m.%d")
fullchain = open('fullchain.pem').read()
request.cert = fullchain
key = open('privkey.pem').read()
request.key = key
response = client.upload_user_certificate(request)
print(UtilClient.to_jsonstring(TeaCore.to_map(response.body)))
