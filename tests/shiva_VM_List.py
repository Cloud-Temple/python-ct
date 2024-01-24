#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Lancer en CMD "pip install requests" pour installer le module

import json
import requests

#INFO
pat_id = "A créer"
pat_secret = "A renseigner à la création du PAT"

#URL
base_url = "https://shiva.cloud-temple.com"
auth_url = base_url + "/api/iam/v2/auth/personal_access_token"
tenant_url = base_url + "/api/iam/v2/tenants"
vm_url = base_url + "/api/compute/v1/vcenters/virtual_machines"

#AUTHENTIFICATION
print("\nAUTHENTIFICATION SHIVA")
headers_auth = {"id": pat_id, "secret": pat_secret}
request_auth = requests.post(auth_url, data=headers_auth)
token = request_auth.text

if request_auth.status_code == 200:
    print("-> Authentification OK")
else:
    print("-> Erreur d'authentification")
    exit()

#REQUEST TENANT ID
print("\nREQUEST 'TENANT ID'")

headers = {'Authorization': 'Bearer ' + token, 'accept': 'application/json'}
request_ten = requests.get(tenant_url, headers=headers)
if request_ten.status_code == 200:
    json_ten = json.loads(request_ten.text)
    for data_ten in json_ten:
        print("-> Nom Tenant : " + data_ten['name'] + " \n-> ID Tenant : " + data_ten['id'] + " \n-> Company ID : " + data_ten['companyId'])
else:
    print("-> Erreur sur la requête TENANT ID")
    exit()

#REQUEST VIRTUAL MACHINES
print("\nREQUEST 'VIRTUAL MACHINES'")

request_vm = requests.get(vm_url, headers=headers)
if request_vm.status_code == 200:
    json_vm = json.loads(request_vm.text)
    print("\nListe des machines virtuelles :")
    for data_vm in json_vm:
        print("-> Nom : " + data_vm['name'] + " \n-> ID : " + data_vm['id'] + " \n-> État : " + data_vm['status'])
        vm_id = data_vm['id']
        vm_info_url = vm_url + "/" + vm_id
        request_vm_info = requests.get(vm_info_url, headers=headers)
        if request_vm_info.status_code == 200:
            json_vm_info = json.loads(request_vm_info.text)
            datacenter_name = json_vm_info.get('datacenterName', '')
            print("-> Datacenter Name: " + datacenter_name)

            dnsName = json_vm_info.get('dnsName', '')
            print("-> Nom DNS: " + dnsName)

            #json_vm_info = json.loads(request_vm_info.text)
            #print("-> json_vm_info:", json_vm_info)  # Debugging statement

            #ip_addresses = json_vm_info.get('ipAddresses', [])
            #print("-> ip_addresses:", ip_addresses)  # Debugging statement

            
            ip_addresses = json_vm_info.get('ipAddresses', [])
            if ip_addresses and 'primary' in ip_addresses:
                primary_ip = ip_addresses['primary']
                print("-> Adresse IP principale : " + primary_ip)
            else:
                print("-> Aucune adresse IP trouvée.")
        else:
            print(f"-> Erreur sur la requête pour obtenir les informations de la machine virtuelle avec l'ID : {vm_id}")
else:
    print("-> Erreur sur la requête VIRTUAL MACHINES")
    exit()
    
