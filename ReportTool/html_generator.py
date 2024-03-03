import pandas as pd
import os
import re

class HtmlGenerator():

    _table_template_path = os.getcwd() + "\\resources\\html_table_template.html"

    def __init__(self):
        return

    def get_replace_value(self, service, column, old_services : pd.DataFrame = None):
        new_value = service[column]
        old_service = old_services.loc[old_services["id"] == service["id"]]
        try:
            if self.old_services.empty:
                return new_value
            if old_service[column].values[0] == new_value:
                return new_value
        except AttributeError:
            print(f"Could not find last value for {column}")
        return f"<mark>{new_value}</mark>"

    def generate_for_all_services(self, services : pd.DataFrame, old_services : pd.DataFrame = None):
        """generates html templates for all services in self.services_df

        Args:
            services (pd.DataFrame): _description_
            old_services (pd.DataFrame, optional): _description_. Defaults to None.

        Returns:
            list<str>: list of html table strings, each defining one service
        """
        if old_services != None:
            old_services_df = self.prepare_data(old_services)
        services_df = self.prepare_data(services)
        html_tables = []
        for _, service in services_df.iterrows():
            html_tables.append(self.generate_for_one_service(service, old_services_df))
        return html_tables

    def generate_for_one_service(self, service : pd.Series, old_services : pd.DataFrame = None):
        """ generates a single html table string for a single service

        Args:
            service (pd.Series): single service dataframe

        Returns:
            str: single html table string for that service.
        """

        html = ""
        with open(self._table_template_path, encoding="utf-8") as template_file:
            html = template_file.read()
        n = len(html)
        search_index = 0
        while search_index < n:
            found_start_index = html.find("{", search_index)
            found_end_index = html.find("}", search_index)
            if found_start_index == -1 or found_end_index == -1:
                break
            value_to_replace = html[found_start_index:found_end_index+1]
            replace_with_value = self.get_replace_value(service, html[found_start_index+1:found_end_index], old_services)
            #replace_with_value = service[html[found_start_index+1:found_end_index]]
            html = html.replace(value_to_replace, replace_with_value)
            search_index = found_end_index+1
            n = len(html)
        return html
    
    def prepare_data(self, services_df : pd.DataFrame):
        services_df["service_name"] = services_df["name"]
        services_df["organisation"] = services_df["organization.name"]
        services_df["description"] = services_df["description"].map(self.remove_html)
        services_df["website"] = services_df["url"]#.map(lambda x: x if x != "" else "404 Website not found")
        #services_df["telephone"] = services_df["contacts"][0][0]["phones"][0]["number"]
        services_df["last_assured_date"] = services_df["pc_metadata.date_assured"]
        return services_df
        
    def remove_html(self, string):
        # maybe keep formatting html such as bold and italics
        p = re.compile(r'<.*?>')
        return p.sub('', string)

def generate_html_tables(services_df : pd.DataFrame, old_services: pd.DataFrame=None):
    gen_html = HtmlGenerator()
    return gen_html.generate_for_all_services(services_df, old_services)


if __name__ == "__main__":
    generate_html_tables(pd.DataFrame({
        "service_name" : ["test service name"],
        "organisation" : ["test organisation"],
        "description" : ["test description"],
        "attending_type" : ["test attending type"],
        "website" : ["test-website.com"],
        "telephone" : ["test telephone"],
        "email" : ["test-email@test.com"],
        "last_assured_date" : ["12/07/2023"],
        }))