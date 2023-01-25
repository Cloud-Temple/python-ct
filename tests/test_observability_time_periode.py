from libs.ShivaApi import Observability

# Init clients
shiva_obs_client = Observability(url="https://shiva.cloud-temple.com",
                                   token_id="<changeme>",
                                   token_secret="<changeme>")

# Show all Appliances
appliances = shiva_obs_client.get_appliances()
print(appliances)
for appliance in appliances:
    print(appliance)

