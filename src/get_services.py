import requests
import pandas as pd
import os

DEFAULT_URL = "https://penninelancs.openplace.directory/o/ServiceDirectoryService/v2/services/"

class GetServices:
    
    def __init__(self, url=DEFAULT_URL, num_services=10):
        self.single_service_url = url
        self.all_services_url = url + f"?per_page={num_services}"
        self.services : pd.DataFrame =pd.DataFrame()    
        
    def get_all_services(self):
        try:
            response = requests.get(self.all_services_url)
        except:
            print("Error fetching all services")
        services = response.json()["content"]
        all_services= []
        #self.services = pd.json_normalize(services, "content")
        for service in services:
            all_services.append(self.get_service(service["id"]))
        self.services = pd.json_normalize(all_services)
        #self.services["service_areas"] = self.services["service_areas"].map(lambda x: pd.json_normalize(x))
        #self.services["service_at_locations"] = self.services["service_at_locations"].map(lambda x: pd.json_normalize(x))
        #self.services["regular_schedules"] = self.services["service_at_locations"].map(lambda x : pd.json_normalize(x["regular_schedules"]))
        #print(self.services["regular_schedules"])
        #self.services["cost_options"] = self.services["cost_options"].map(lambda x: pd.json_normalize(x))
        #self.services["contacts"] = self.services["contacts"].map(lambda x: pd.json_normalize(x))
        #self.services["service_taxonomys"] = self.services["service_taxonomys"].map(lambda x: pd.json_normalize(x))
        
            
    def get_services_by_ids(self, ids : list):
        all_services = []
        for id in ids:
            all_services.append(self.get_service(id))
        self.services = pd.json_normalize(all_services)
        return self.services

    def get_service(self, id):
        try:
            response = requests.get(self.single_service_url + id)
        except:
            print("Error fetching service " + id)
        return response.json()
    
    
def get_services_from_api(url):
    get_services = GetServices(url)
    get_services.get_all_services()
    return get_services.services

def get_services_by_client(client, url=DEFAULT_URL):
    client_services_df = pd.read_csv("resources\\data\\clientsServiceIds.csv")
    services = list(client_services_df[client])
    return GetServices(url).get_services_by_ids(services)
    