import json
from http import HTTPStatus
from libs.httpClient import HttpClient


class Compute(HttpClient):
    def __init__(self, url: str, token_id: str, token_secret: str):
        super().__init__(url=url, token_id=token_id, token_secret=token_secret)
        self.base_url = "/api/compute"
        self.auth()

    def get_vms(self):
        """Find virtual machines"""
        response = self.get(self.base_url + "/v1/vcenters/virtual_machines")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_vm_infos(self, virtual_machine_id: str):
        """Find virtual machine info"""
        response = self.get(self.base_url + "/v1/vcenters/virtual_machines/%s" % virtual_machine_id)
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_vm_infos_by_vdc(self, vdc_id: str):
        """Find virtual machine with Virtual Datacenter ID Filter"""
        response = self.get(self.base_url + "/v1/vcenters/virtual_machines?datacenters[]=" + vdc_id)
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_vm_disk(self, vm_id: str):
        """Find Disks for virtual machine"""
        response = self.get(self.base_url + "/v1/vcenters/virtual_disks?virtualMachineId=" + vm_id)
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def power_on_vm(self, virtual_machine_id):
        response = self.patch(self.base_url + "/v1/vcenters/virtual_machines/power",
                              data={'id': virtual_machine_id, 'powerAction': 'on'})

        if response.status_code == HTTPStatus.OK:
            return {"status": "success"}
        return self.error_response(response)

    def power_off_vm(self, virtual_machine_id):
        response = self.patch(self.base_url + "/v1/vcenters/virtual_machines/power",
                              data={'id': virtual_machine_id, 'powerAction': 'off'})

        if response.status_code == HTTPStatus.OK:
            return {"status": "success"}
        return self.error_response(response)

    def create_vm_with_template(self, vcenter_version: str, content_libraries: str, contentLibraryItemId: str, hostClusterId: str,
                                datastoreId: str, deployOptions: [], datacenterId: str, virtual_machine_name: str):

        json_data = {"contentLibraryItemId": contentLibraryItemId, "name": virtual_machine_name,
                     "hostClusterId": hostClusterId, "datastoreId": datastoreId, "deployOptions": deployOptions,
                     "datacenterId": datacenterId}

        response = self.post(self.base_url + f"/v1/vcenters/{vcenter_version}/content_libraries/{content_libraries}/items",
                             data=json_data)

        if response.status_code == HTTPStatus.CREATED:
            return {"status": "success"}
        return self.error_response(response)

    def get_hosts(self):
        """Find Hots"""
        response = self.get(self.base_url + "/v1/vcenters/hosts")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)
    
    def get_hosts_by_vdc(self, vdc_id):
        """Find Hots with Virtual Datacenter ID Filter"""
        response = self.get(self.base_url + "/v1/vcenters/hosts?virtualDatacenterId="+vdc_id)
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_host_clusters(self):
        """Find Hots"""
        response = self.get(self.base_url + "/v1/vcenters/host_clusters")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)
    
    def get_host_clusters_by_vdc(self,id_vdc):
        """Find Hots with Virtual Datacenter ID Filter"""
        response = self.get(self.base_url + "/v1/vcenters/host_clusters?virtualDatacenterId="+id_vdc)
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_datastores(self):
        """Find Datastores"""
        response = self.get(self.base_url + "/v1/vcenters/datastores")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)
    
    def get_datastores_by_dsclus(self, id_ds_clus):
        """Find Datastores"""
        response = self.get(self.base_url + "/v1/vcenters/datastores?datastoreClusterId=" +id_ds_clus)
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_datastore_clusters(self):
        """Find Datastore Clusters"""
        response = self.get(self.base_url + "/v1/vcenters/datastore_clusters")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)
    
    def get_datastore_clusters_by_dc(self, id_dc):
        """Find Datastore Clusters"""
        response = self.get(self.base_url + "/v1/vcenters/datastore_clusters?virtualDatacenterId="+id_dc)
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_vcenters(self):
        """Find vCenter servers"""
        response = self.get(self.base_url + "/v1/vcenters")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)
    
    def get_ressource_pools(self):
        """Find Ressources Pools"""
        response = self.get(self.base_url + "/v1/vcenters/resource_pools")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_virtual_dc(self):
        """Find Virtual Datacenters"""
        response = self.get(self.base_url + "/v1/vcenters/virtual_datacenters")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)


class Iam(HttpClient):
    def __init__(self, url: str, token_id: str, token_secret: str):
        super().__init__(url=url, token_id=token_id, token_secret=token_secret)
        self.base_url = "/api/iam"
        self.auth()

    def get_users(self):
        """Get Users"""
        response = self.get(self.base_url + "/v2/users?companyId=" + self.jwt_decoded['companyId'])
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_users_assignments(self, user_id: str = None):
        if not user_id:
            user_id = self.jwt_decoded['userId']
        """Get User Assignments"""
        response = self.get(self.base_url + "/v2/assignments/tenant?tenantId=" + self.jwt_decoded['scope']['id']
                            + "&userId=" + user_id)
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)


class Inventory(HttpClient):
    def __init__(self, url: str, token_id: str, token_secret: str):
        super().__init__(url=url, token_id=token_id, token_secret=token_secret)
        self.base_url = "/api/inventory"
        self.auth()

    def get_virtual_machines(self):
        """Get all Virtual Machines"""
        response = self.get(self.base_url + "/v1/virtual_machines")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def find_virtual_machine(self, name: str):
        """Find Virtual Machine"""
        response = self.get(self.base_url + "/v1/virtual_machines")
        if response.status_code == HTTPStatus.OK:
            for vm in response.json().get('items'):
                if vm.get('name') == name:
                    return vm
            return None
        return self.error_response(response)

    def get_applications(self):
        """Get all inventoried application"""
        response = self.get(self.base_url + "/v1/applications")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def create_application(self, application_name: str, application_version: str):
        """Create application"""
        data = {"typeId": "5c2d444e-f80c-42b2-b149-6d3017d4b426", "items":
            [{"name": application_name, "version": application_version}]}
        response = self.post(self.base_url + "/v1/inventories/items", data)
        if response.status_code == HTTPStatus.CREATED:
            return True
        return self.error_response(response)

    def update_item(self, data: {}):
        """Update item"""
        response = self.patch(self.base_url + "/v1/inventories/items", data)
        if response.status_code == HTTPStatus.CREATED:
            return True
        return self.error_response(response)


class Backup(HttpClient):
    def __init__(self, url: str, token_id: str, token_secret: str):
        super().__init__(url=url, token_id=token_id, token_secret=token_secret)
        self.base_url = "/api/backup"
        self.auth()

    def get_reports(self):
        """Find Backup reports"""
        response = self.get(self.base_url + "/v1/reports")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_jobs(self):
        """Find Backup jobs"""
        response = self.get(self.base_url + "/v1/jobs")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_policies(self):
        """Find SLA Policies"""
        response = self.get(self.base_url + "/v1/policies")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_spp_servers(self):
        """Find SPP Servers"""
        response = self.get(self.base_url + "/v1/spp_servers?tenantId=" + self.jwt_decoded['scope']['id'])
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_spp_server(self, id: str):
        """Find SPP Server"""
        response = self.get(self.base_url + "/v1/spp_servers/"+id )
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def get_storages(self):
        """Find SPP Storages"""
        response = self.get(self.base_url + "/v1/storages")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)


class Tags(HttpClient):
    def __init__(self, url: str, token_id: str, token_secret: str):
        super().__init__(url=url, token_id=token_id, token_secret=token_secret)
        self.base_url = "/api/tag"
        self.auth()

    def get_tags(self):
        """Retrieve all tags"""
        response = self.get(self.base_url + "/v1/tags")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)


class Observability(HttpClient):
    def __init__(self, url: str, token_id: str, token_secret: str):
        super().__init__(url=url, token_id=token_id, token_secret=token_secret)
        self.base_url = "/api/rtms"
        self.auth()

    def get_appliances(self):
        """Get all Appliances"""
        response = self.get(self.base_url + "/v1/appliances")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response).get('data')
        return self.error_response(response)

    def get_hosts(self, name: str = None):
        """Get a list of hosts."""
        response = self.get(self.base_url + "/v1/hosts")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)

    def find_host(self, name: str):
        """Find Virtual Machine"""
        response = self.get(self.base_url + "/v1/hosts?name=" + name)
        if response.status_code == HTTPStatus.OK:
            for host in response.json().get('data'):
                if host.get('name') == name:
                    return host
            return None
        return self.error_response(response)
    
    def get_host_services(self, id_host: str):
        """Get a list of services for a host """
        response = self.get(self.base_url + "/v1/hosts/" + id_host + "/services")
        if response.status_code == HTTPStatus.OK:
            return self.json_response(response)
        return self.error_response(response)
    
    def disable_notifications_by_service(self, id_host: str, id_service: str):
        """Disable service notifications"""
        data = {"enable": False, "services":
            [id_service]}
        print(data)
        response = self.post(self.base_url + "/v1/hosts/" + id_host + "/monitoring/notifications", data)
        if response.status_code == HTTPStatus.CREATED:
            return True
        return self.error_response(response)
        
    def enable_notifications_by_service(self, id_host: str, id_service: str):
        """Disable service notifications"""
        data = {"enable": True, "services":
            [id_service]}
        print(data)
        response = self.post(self.base_url + "/v1/hosts/" + id_host + "/monitoring/notifications", data)
        if response.status_code == HTTPStatus.CREATED:
            return True
        return self.error_response(response)
    
    
    #
    # def create_application(self, application_name: str, application_version: str):
    #     """Create application"""
    #     data = {"typeId": "5c2d444e-f80c-42b2-b149-6d3017d4b426", "items":
    #         [{"name": application_name, "version": application_version}]}
    #     response = self.post(self.base_url + "/v1/inventories/items", data)
    #     if response.status_code == HTTPStatus.CREATED:
    #         return True
    #     return self.error_response(response)
    #
    # def update_item(self, data: {}):
    #     """Update item"""
    #     response = self.patch(self.base_url + "/v1/inventories/items", data)
    #     if response.status_code == HTTPStatus.CREATED:
    #         return True
    #     return self.error_response(response)
