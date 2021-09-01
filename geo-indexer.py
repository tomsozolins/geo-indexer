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
            "selectGroups": "extend"
        }
    )['result']
    zapi.user.logout()
    return zabbix_data


async def create_index():
    await es.indices.create(index='geo-hosts', ignore=400)


async def delete_documents():
    await es.delete_by_query(index='geo-hosts', body={"query": {"match_all": {}}})


async def update_index_mapping():
    await es.indices.put_mapping(index='geo-hosts', ignore=400, body={"properties": {"coordinates": {"type": "geo_point"}}})


async def check_key(host, key):
    try:
        return host['inventory'][key]
    except TypeError:
        return ""

async def gendata():
    
    for host in zabbix_data:
        yield {
            "_index": "geo-hosts",
            "_id": host["hostid"],
            "group": host["groups"][0]["name"],
            "host": host["host"],
            "hostid": host["hostid"],
            "interface_ip": host["interfaces"][0]["ip"],
            "alias": await check_key(host, 'alias'),
            "asset_tag": await check_key(host, 'asset_tag'),
            "chassis": await check_key(host, 'chassis'),
            "contact": await check_key(host, 'contact'),
            "contract_number": await check_key(host, 'contract_number'),
            "date_hw_decomm": await check_key(host, 'date_hw_decomm'),
            "date_hw_expiry": await check_key(host, 'date_hw_expiry'),
            "date_hw_install": await check_key(host, 'date_hw_install'),
            "date_hw_purchase": await check_key(host, 'date_hw_purchase'),
            "deployment_status": await check_key(host, 'deployment_status'),
            "hardware": await check_key(host, 'hardware'),
            "hardware_full": await check_key(host, 'hardware_full'),
            "host_netmask": await check_key(host, 'host_netmask'),
            "host_networks": await check_key(host, 'host_networks'),
            "host_router": await check_key(host, 'host_router'),
            "hw_arch": await check_key(host, 'hw_arch'),
            "installer_name": await check_key(host, 'installer_name'),
            "location_lat": await check_key(host, 'location_lat'),
            "location_lon": await check_key(host, 'location_lon'),
            "macaddress_a": await check_key(host, 'macaddress_a'),
            "macaddress_b": await check_key(host, 'macaddress_b'),
            "model": await check_key(host, 'model'),
            "name": await check_key(host, 'name'),
            "notes": await check_key(host, 'notes'),
            "oob_ip": await check_key(host, 'oob_ip'),
            "oob_netmask": await check_key(host, 'oob_netmask'),
            "oob_router": await check_key(host, 'oob_router'),
            "os": await check_key(host, 'os'),
            "os_full": await check_key(host, 'os_full'),
            "os_short": await check_key(host, 'os_short'),
            "poc_1_cell": await check_key(host, 'poc_1_cell'),
            "poc_1_email": await check_key(host, 'poc_1_email'),
            "poc_1_name": await check_key(host, 'poc_1_name'),
            "poc_1_notes": await check_key(host, 'poc_1_notes'),
            "poc_1_phone_a": await check_key(host, 'poc_1_phone_a'),
            "poc_1_phone_b": await check_key(host, 'poc_1_phone_b'),
            "poc_1_screen": await check_key(host, 'poc_1_screen'),
            "poc_2_cell": await check_key(host, 'poc_2_cell'),
            "poc_2_email": await check_key(host, 'poc_2_email'),
            "poc_2_name": await check_key(host, 'poc_2_name'),
            "poc_2_notes": await check_key(host, 'poc_2_notes'),
            "poc_2_phone_a": await check_key(host, 'poc_2_phone_a'),
            "poc_2_phone_b": await check_key(host, 'poc_2_phone_b'),
            "poc_2_screen": await check_key(host, 'poc_2_screen'),
            "serialno_a": await check_key(host, 'serialno_a'),
            "serialno_b": await check_key(host, 'serialno_b'),
            "site_address_a": await check_key(host, 'site_address_a'),
            "site_address_b": await check_key(host, 'site_address_b'),
            "site_address_c": await check_key(host, 'site_address_c'),
            "site_city": await check_key(host, 'site_city'),
            "site_country": await check_key(host, 'site_country'),
            "site_notes": await check_key(host, 'site_notes'),
            "site_rack": await check_key(host, 'site_rack'),
            "site_state": await check_key(host, 'site_state'),
            "site_zip": await check_key(host, 'site_zip'),
            "software": await check_key(host, 'software'),
            "software_app_a": await check_key(host, 'software_app_a'),
            "software_app_b": await check_key(host, 'software_app_b'),
            "software_app_c": await check_key(host, 'software_app_c'),
            "software_app_d": await check_key(host, 'software_app_d'),
            "software_app_e": await check_key(host, 'software_app_e'),
            "software_full": await check_key(host, 'software_full'),
            "tag": await check_key(host, 'tag'),
            "type": await check_key(host, 'type'),
            "type_full": await check_key(host, 'type_full'),
            "url_a": await check_key(host, 'url_a'),
            "url_b": await check_key(host, 'url_b'),
            "url_c": await check_key(host, 'url_c'),
            "vendor": await check_key(host, 'vendor'),
            "inventory_mode": host["inventory_mode"],
            "name": host["name"],
            "snmp_available": host["snmp_available"],
            "status": host["status"],

        }

es = AsyncElasticsearch(
    [ELASTIC_ENDPOINT],
    http_auth=(ELASTIC_USER, ELASTIC_PASS),
    verify_certs=False,
    ssl_show_warn=False
)

zabbix_data = get_zabbix_data()

async def main():
    start = time.time()

    await create_index()
    await delete_documents()
    await update_index_mapping()
    await async_bulk(es, gendata())

    end = time.time()
    logging.info(f"Execution time {round(end - start, 2)} seconds")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
