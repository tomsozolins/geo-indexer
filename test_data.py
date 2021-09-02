import urllib3
from pyzabbix import ZabbixAPI
import asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
import logging
import sys
import os
import time

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# load env variables
ZABBIX_ENDPOINT = os.getenv("ZABBIX_ENDPOINT")
ZABBIX_USER = os.getenv("ZABBIX_USER")
ZABBIX_PASS = os.getenv("ZABBIX_PASS")
ELASTIC_ENDPOINT = os.getenv("ELASTIC_ENDPOINT")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_PASS = os.getenv("ELASTIC_PASS")



def get_zabbix_data():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    zapi = ZabbixAPI(ZABBIX_ENDPOINT, detect_version=False)
    zapi.session.verify = False
    zapi.login(ZABBIX_USER, ZABBIX_PASS)
    zabbix_data = zapi.do_request(
        "host.get",
        {
            "output": "extend",
            "selectParentTemplates": [
                "templateid",
                "name"
            ],
            "selectInterfaces": "extend",
            "selectInventory": "extend",
            "selectTriggers": "extend",
            "selectGroups": "extend",
            "filter": {"host": "13-janvara15-ptz"}
        }
    )['result']
    zapi.user.logout()
    return zabbix_data


from pprint import pprint

pprint(get_zabbix_data())
