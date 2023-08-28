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

#CREATE SNAPSHOT
create_snapshot_url = base_url + "/api/compute/v1/vcenters/snapshots"

snapshot_data = {
    "virtualMachineId": "xxxxxxxxxx",  # Replace with the actual virtual machine ID
    "name": "test",
    "description": "Snapshot test",
    "quiesce": False,
    "memory": False
}

print("\nCREATING SNAPSHOT")

request_create_snapshot = requests.post(create_snapshot_url, headers=headers, json=snapshot_data)

if request_create_snapshot.status_code == 201:
    print("-> Snapshot created successfully.")
else:
    print("-> Error creating snapshot.")
    print("-> Response:", request_create_snapshot.text)
    exit()
