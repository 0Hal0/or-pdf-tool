"""Module for the ServiceManager class"""
import os
import requests
import pandas as pd

DEFAULT_URL = "https://penninelancs.openplace.directory/o/ServiceDirectoryService/v2/services/"
SERVICE_SAVE_PATH = "resources\\data\\"

class ServiceManager:
    """Class used to get and save services associated with a user
    """
    def __init__(self, url=DEFAULT_URL, num_services=10):
        self.single_service_url = url
        self.all_services_url = url + f"?per_page={num_services}"
        self.services : pd.DataFrame =pd.DataFrame()

    def get_all_services(self):
        """ (deprecated) Function gets all services in no order up to the limit num_services
        """
        try:
            response = requests.get(self.all_services_url, timeout=120)
        except requests.exceptions.RequestException as e:
            print("Error fetching all services" + e.strerror)
        services = response.json()["content"]
        all_services= []
        #self.services = pd.json_normalize(services, "content")
        for service in services:
            all_services.append(self.get_service(service["id"]))
        self.services = pd.json_normalize(all_services)


    def get_services_by_ids(self, ids : list):
        """Gets service information by list of ids

        Args:
            ids (list): List of service ids

        Returns:
            pd.DataFrame: Dataframe of service information
        """
        all_services = []
        for service_id in ids:
            all_services.append(self.get_service(service_id))
        self.services = pd.json_normalize(all_services)
        return self.services

    def get_service(self, service_id : str):
        """Get single service by id

        Args:
            service_id (str): id of service to get

        Returns:
            JSON: json containing service information
        """
        try:
            response = requests.get(self.single_service_url + service_id, timeout=60)
        except requests.exceptions.RequestException as e:
            print("Error fetching service " + service_id)
            return Exception("Error fetching services" + e.strerror)
        return response.json()

    def get_services_for_user(self, user : str):
        """Get the last retrieved services for a given user

        Args:
            user (str): name of the user

        Returns:
            pd.DataFrame: dataframe of service information 
        """
        df = self.try_get_last_services(user)
        return self.get_services_by_ids(df["id"].to_list())

    def get_save_path(self, user : str):
        """Gets the path to save service history for a given user"""
        return f"{SERVICE_SAVE_PATH}{user}.parquet"

    def try_get_last_services(self, user : str):
        """Gets the last saved services for a given user"""
        save_path = self.get_save_path(user)
        if os.path.exists(save_path):
            df = pd.read_parquet(save_path)
            return df
        raise ValueError("Error: Could not find any services for given user, try adding services first")

    def save_services(self, services_df : pd.DataFrame, user : str):
        """Saves the given services for a given user"""
        services_df.to_parquet(self.get_save_path(user))
        return


def get_services_from_api(url):
    """ (deprecated) Gets all service from the specified API

    Args:
        url (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    get_services = ServiceManager(url)
    get_services.get_all_services()
    return get_services.services

def get_services_by_client(client, url=DEFAULT_URL):
    """ (depracated)

    Args:
        client (_type_): _description_
        url (_type_, optional): _description_. Defaults to DEFAULT_URL.

    Returns:
        _type_: _description_
    """
    client_services_df = pd.read_csv("resources\\data\\clientsServiceIds.csv")
    services = list(client_services_df[client])
    return ServiceManager(url).get_services_by_ids(services)

def get_services_for_user(user : str):
    return ServiceManager().try_get_last_services(user)

def add_services_for_user(user :str, services : list[str]):
    path = ServiceManager().get_save_path(user)
    df = pd.DataFrame({"id": services})
    df["id"] = df["id"].astype("str")
    if os.path.exists(path):
        existing_df = pd.read_parquet(path)
        existing_df["id"] = existing_df["id"].astype("str")
        df = df.merge(existing_df, on="id", how="left")
    df.to_parquet(path)
