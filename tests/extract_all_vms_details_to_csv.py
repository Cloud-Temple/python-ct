import json
import concurrent.futures
import pandas as pd

from libs.ShivaApi import Compute

# Init clients
shiva_compute_client = Compute(url="https://shiva.cloud-temple.com",
                               token_id="",
                               token_secret="")

# Libs
def __extract_vm_infos(vm_name: str, vm_id: str, vm_list_data: [], vm_disk_list_data: []):

    try:
        vm_infos = shiva_compute_client.get_vm_infos(vm_id)

        print(f"retreive info for vm : {vm_infos.get('name')}")

        if vm_infos.get('ipAddresses').get('primary'):
            vm_infos['ipAddresses_primary'] = vm_infos['ipAddresses']['primary']
        else:
            vm_infos['ipAddresses_primary'] = None

        network_primary = shiva_compute_client.get_vm_network_adapters(vm_id)
        vm_infos['network_primary'] = network_primary

        vm_disks = shiva_compute_client.get_vm_disk(vm_id)
        vm_infos['vm_disk'] = vm_disks

        for vm_disk in vm_disks:
            vm_disk_list_data.append({
            'name': vm_infos.get('name'),
            'powerState': vm_infos.get('powerState'),
            'datacenterName': vm_infos.get('datacenterName'),
            'disk_name': vm_disk.get('name'),
            'disk_capacity': vm_disk.get('capacity'),
            'datastore_name': vm_disk.get('datastoreName'),
            'disk_instant_access': vm_disk.get('instantAccess'),
            'disk_path': vm_disk.get('diskPath'),
            'provisioning_type': vm_disk.get('provisioningType'),
            'disk_mode': vm_disk.get('diskMode'),
            })

        vm_list_data.append({
            'name': vm_infos.get('name'),
            'powerState': vm_infos.get('powerState'),
            'datacenterName': vm_infos.get('datacenterName'),
            'esxcluster': vm_infos.get('hostClusterName'),
            'esxname': vm_infos.get('hostName'),
            'datastoreClusterName': vm_infos.get('datastoreClusterName'),
            'datastoreName': vm_infos.get('datastoreName'),
            'hardwareVersion': vm_infos.get('hardwareVersion'),
            'operatingSystemName': vm_infos.get('operatingSystemName'),
            'cpu': vm_infos.get('cpu'),
            'memory': vm_infos.get('memory'),
            'balloonedMemory': vm_infos.get('balloonedMemory'),
            'compressedMemory': vm_infos.get('compressedMemory'),
            'swappedMemory': vm_infos.get('swappedMemory'),
            'tools': vm_infos.get('tools'),
            'toolsVersion': vm_infos.get('toolsVersion'),
            'toolsMode': vm_infos.get('toolsMode'),
            'snapshoted': vm_infos.get('snapshoted'),
            'storage_committed': vm_infos.get('storage').get('committed'),
            'storage_uncommitted': vm_infos.get('storage').get('uncommitted'),
            'triggered_alarms_count': len(vm_infos.get('triggeredAlarms')),
            'disk_count': len(vm_disks),
            'ipAddresses_primary': vm_infos.get('ipAddresses_primary'),
            'dnsName': vm_infos.get('dnsName')
        })

        print(json.dumps(vm_infos))

        return f" extracted vm infos : {vm_name} OK "

    except Exception as err:
        print(f"errr {err}")
        return f" extracted vm infos : {vm_name} KO "


def __convert_list_to_dict(vms_list: []):
    vms_dict = {}
    # Convert
    for vm in vms_list:
        print(f"Virtual machine {vm['name']}")
        print()

        vms_dict[vm.get('id')] = vm
    return vms_dict

# Init vars
vms_list = shiva_compute_client.get_vms()

vms_dict = __convert_list_to_dict(vms_list=vms_list)

# get vm infos
vms_dict_data = []
vm_disk_list_data = []

# Start Thread loop
with concurrent.futures.ThreadPoolExecutor(50) as executor:
    futures = []
    # Loop on tickets
    for k_vm, vm in vms_dict.items():
        print(f"k_vm_id : {k_vm}")
        futures.append(executor.submit(__extract_vm_infos, vm_name=vm.get('name'), vm_id=k_vm,
                                       vm_list_data=vms_dict_data, vm_disk_list_data=vm_disk_list_data))

    for future in concurrent.futures.as_completed(futures):
        print(f"future result : {future.result()}")

print(json.dumps(vms_dict_data))

# Convert VM list into dataframe and into Excel
vm_df = pd.DataFrame(data=vms_dict_data)
vm_df.to_excel("vms_dict_data.xlsx", index=False)

# Convert VM list into dataframe and into Excel
disk_df = pd.DataFrame(data=vm_disk_list_data)
disk_df.to_excel("vm_disk_list_data.xlsx", index=False)
