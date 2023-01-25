from libs.ShivaApi import Inventory

# Init clients
shiva_inventory_client = Inventory(url="https://shiva.cloud-temple.com",
                                   token_id="5a20ca1c-028c-46e8-8bea-6a0a0a6b8c7e",
                                   token_secret="d27f838d-78f4-4873-ac4c-c98b68a995f4")

# Show all Applications
applications = shiva_inventory_client.get_applications()
print(applications)
for application in applications.get('items'):
    print(application)


# Show all Virtual machine
virtual_machines = shiva_inventory_client.get_virtual_machines()
print(virtual_machines)
for virtual_machine in virtual_machines.get('items'):
    #print(virtual_machine)
    print(f"Virtual machine {virtual_machine.get('name')} with {virtual_machine.get('cpu')} CPU is managed by {virtual_machine.get('manager_name')}")

