from libs.ShivaApi import Compute

# Init clients
shiva_compute_client = Compute(url="https://shiva.cloud-temple.com",
                               token_id="",
                               token_secret="")

# Show all Virtual machine
datastores = shiva_compute_client.get_datastores()

for datastore in datastores:
    if datastore.get('name') == "":
        print(datastore)

        print(f"maxCapacity {datastore.get('maxCapacity') / 1024 / 1024 / 1024}")
        print(f"freeCapacity {datastore.get('freeCapacity') / 1024 / 1024 / 1024}")

        print(f"use : {(datastore.get('maxCapacity') - datastore.get('freeCapacity')) / 1024 / 1024 / 1024}")
        print(datastore.get('freeCapacity') / datastore.get('maxCapacity') * 100)
