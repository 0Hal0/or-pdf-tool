"""Module for the ServiceManager class"""
import os
import re
import requests
import pandas as pd

DEFAULT_URL = "https://penninelancs.openplace.directory/o/ServiceDirectoryService/v2/services/"
SERVICE_SAVE_PATH = "resources\\data\\"

class ServiceManager:
    """Class used to get and save services associated with a user
    """
    def __init__(self, url=DEFAULT_URL):
        self.single_service_url = url
        self.paginated_services_url = url
        self.services : pd.DataFrame =pd.DataFrame()

    def get_all_services(self):
        """ (deprecated) Function gets all services in no order up to the limit num_services
        """
        all_services = []
        try:
            response = requests.get(self.paginated_services_url, timeout=120).json()
        except requests.exceptions.RequestException as e:
            print("Error fetching all services" + e.strerror)
        for i in range(2, response["totalPages"]):
            all_services = response["content"]
            try:
                response = requests.get(self.paginated_services_url+f"?page={str(i)}", timeout=120).json()
            except requests.exceptions.RequestException as e:
                print("Error fetching all services" + e.strerror)

        services_df = pd.json_normalize(all_services)

        return services_df

    def get_all_services_detailed(self):
        """ (deprecated) Function gets all services in no order up to the limit num_services
        """
        all_services = []
        i=1
        try:
            response = requests.get(self.paginated_services_url, timeout=120).json()
        except requests.exceptions.RequestException as e:
            print("Error fetching all services" + e.strerror)
        services = []
        for i in range(2, response["totalPages"] + 1):
            services = response["content"]
            for service in services:
                all_services.append(self.get_service(service["id"]))
            try:
                response = requests.get(self.paginated_services_url+f"?page={str(i)}", timeout=120).json()
            except requests.exceptions.RequestException as e:
                print("Error fetching all services" + e.strerror)


        services_df = pd.json_normalize(all_services)

        print(services_df)

        services_df.to_csv("test\\test.csv")


    def get_services_by_ids(self, ids : list):
        """Gets service information by list of ids

        Args:
            ids (list): List of service ids

        Returns:
            pd.DataFrame: Dataframe of service information
        """
        all_services = []
        for service_id in ids:
            try:
                all_services.append(self.get_service(service_id))
            except requests.exceptions.RequestException as e:
                print(e.strerror)
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
            response = requests.get(self.single_service_url + service_id, timeout=10)
        except requests.exceptions.RequestException as e:
            print("Error fetching service " + service_id)
            raise e
        return response.json()

    def get_services_for_user(self, user : str):
        """Get the last retrieved services for a given user

        Args:
            user (str): name of the user

        Returns:
            pd.DataFrame: dataframe of service information 
        """
        ids = self.get_service_ids_for_user(user)
        return self.prepare_data(self.get_services_by_ids(ids))

    def get_save_path(self, user : str):
        """Gets the path to save service history for a given user"""
        return f"{SERVICE_SAVE_PATH}{user}.parquet"

    def get_service_ids_for_user(self, user: str):
        """Gets a list of service ids for the given user"""
        save_path = self.get_save_path(user)
        if os.path.exists(save_path):
            df = pd.read_parquet(save_path)
            return df["id"].to_list()
        raise ValueError("Error: Could not find any services for given user, try adding services first")

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
    
    def prepare_data(self, services_df : pd.DataFrame):
        df = pd.DataFrame()
        df["id"] = services_df["id"]
        if "name" in services_df:
            df["service_name"] = services_df["name"]
        else:
            df["service_name"] = "404 Could not find service name"
            return df
        if "organization.name" in services_df:
            df["organisation"] = services_df["organization.name"]
        else:
            df["organisation"] = ""
        if "description" in services_df:
            df["description"] = services_df["description"].map(self.remove_html)
        else:
            df["description"] = ""
        if "attending_type" in services_df:
            df["attending_type"] = services_df["attending_type"]
        else:
            df["attending_type"] = ""
        if "url" in services_df:
            df["website"] = services_df["url"]#.map(lambda x: x if x != "" else "404 Website not found")
        #services_df["telephone"] = services_df["contacts"][0][0]["phones"][0]["number"]
        try:
            df["telephone"] = services_df["contacts"][0][0]["phones"][0]["number"]
        except KeyError:
            df["telephone"] = ""
        except ValueError:
            df["telephone"] = ""
        except ArithmeticError:
            df["telephone"] = ""
        except Exception:
            df["telephone"] = ""
        if "email" in services_df:
            df["email"] = services_df["email"]
        else:
            df["email"] = ""
        if "pc_metadata.date_assured" in services_df:
            df["last_assured_date"] = services_df["pc_metadata.date_assured"]
        else:
            df["last_assured_date"] = ""
        return df
    
    def remove_html(self, string):
        # maybe keep formatting html such as bold and italics
        p = re.compile(r'<.*?>')
        return p.sub('', string)

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
