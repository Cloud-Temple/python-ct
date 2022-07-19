from libs.ShivaApi import Inventory

# Init clients
shiva_inventory_client = Inventory(url="https://shiva.cloud-temple.com",
                                   token_id="<changeme>",
                                   token_secret="<changeme>")

# Show all Virtual machine
types = shiva_inventory_client.get_types()

for type in types:
    if type.get('name') == "application":
        for application in shiva_inventory_client.get_application_items(inventory_item_type=type.get('uuid')).get('items'):
            print(f"Application {application.get('name')}")
            for vmuuid in application.get('vm'):
                print(f"vm uuid : {vmuuid}")
