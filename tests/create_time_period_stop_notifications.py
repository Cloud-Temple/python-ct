from libs.ShivaApi import Observability

# Init clients
shiva_observability_client = Observability(url="https://shiva.cloud-temple.com",
                               token_id="[change_me]",
                               token_secret="[change_me]")

# Get host id from monitoring
host = shiva_observability_client.find_host("[host_name]")
id = host.get('id')

# Get all services id for specified host
services = shiva_observability_client.get_host_services(str(id))

for service in services.get('data'):
    time_period ={
      "name": "Monitoring service TimePeriodStop",
      "reason": "Back up of database",
      "timePeriodStart": "2022-03-21",
      "timePeriodEnd": "2022-03-25",
      "monitoringServices": [service.get('id')],
      "monday": [
        {
          "from": "05:00",
          "to": "06:00"
        }
      ]
    }
    
    time_period_stop = shiva_observability_client.create_time_period_stop(time_period)
    print("Host " + host.get('name') + " - Time period stop created for " + str(service.get('id')) + " service" )
