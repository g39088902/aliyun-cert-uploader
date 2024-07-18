# -*- coding: utf-8 -*-
import os
import datetime
from Tea.core import TeaCore
from alibabacloud_cas20200407.client import Client as CasClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cas20200407 import models as cas_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_dcdn20180115.client import Client as DcdnClient
from alibabacloud_dcdn20180115 import models as dcdn_models


config = open_api_models.Config()
config.access_key_id = os.getenv('ACCESS_KEY_ID')
config.access_key_secret = os.getenv('ACCESS_KEY_SECRET')
config.endpoint = 'cas.aliyuncs.com'
today = datetime.date.today().strftime("%Y.%m.%d")
casClient = CasClient(config)
request = cas_models.UploadUserCertificateRequest()
request.name = today
fullchain = open('fullchain.pem').read()
request.cert = fullchain
key = open('privkey.pem').read()
request.key = key
response = casClient.upload_user_certificate(request)
print(UtilClient.to_jsonstring(TeaCore.to_map(response.body)))


config = open_api_models.Config()
config.access_key_id = os.getenv('ACCESS_KEY_ID')
config.access_key_secret = os.getenv('ACCESS_KEY_SECRET')
config.region_id = "cn-hangzhou"
dcdnClient = DcdnClient(config)
request = dcdn_models.BatchSetDcdnDomainCertificateRequest()
request.cert_name = today
request.cert_type = "cas"
domains = open("dcdn_domains.txt").read().split("\n")
domains.remove("")
request.domain_name = ",".join(domains)
request.sslprotocol = "on"
try:
    response = dcdnClient.batch_set_dcdn_domain_certificate(request)
    print('-------批量设置加速域名证书信息成功--------')
    print(UtilClient.to_jsonstring(TeaCore.to_map(response.body)))
except Exception as error:
    print(error.message)