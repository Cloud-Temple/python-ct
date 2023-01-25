from libs.ShivaApi import Observability

# Init clients
shiva_obs_client = Observability(url="https://shiva.cloud-temple.com",
                                   token_id="5a20ca1c-028c-46e8-8bea-6a0a0a6b8c7e",
                                   token_secret="d27f838d-78f4-4873-ac4c-c98b68a995f4")

# Show all Appliances
appliances = shiva_obs_client.get_appliances()
print(appliances)
for appliance in appliances:
    print(appliance)

