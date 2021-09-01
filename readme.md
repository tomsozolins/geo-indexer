## Geo indexer
#### Create kubernetes secret
```
# kubectl create secret generic zabbix-endpoint-user-pass \
  --from-literal=zabbix_endpoint='<ZABBIX-ENDPOINT>' \
  --from-literal=zabbix_user=<ZABBIX-USERNAME> \
  --from-literal=zabbix_pass='<ZABBIX-PASSWORD>'
```
#### Deploy geo-indexer
```
# kubectl apply -f geo-indexer.yaml
```
