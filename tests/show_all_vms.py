from libs.ShivaApi import Compute

# Init clients
shiva_compute_client = Compute(url="https://shiva.cloud-temple.com",
                               token_id="<changeme>",
                               token_secret="<changeme>")

# Show all Virtual machine
vms_list = shiva_compute_client.get_vms()

for vm in vms_list:
    print(vm)
    print("A virtual machine %s is %s" % (vm['name'], vm['powerState']))
