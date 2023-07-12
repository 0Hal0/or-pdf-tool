import pandas as pd
import os

class GenerateHTMLTables():

    _table_template_path = os.getcwd() + "\\resources\\html_table_template.html"

    def __init__(self, services : pd.DataFrame):
        self.services_df = services

    def generate_for_all_services(self):
        """ generates html templates for all services in self.services_df

        Returns:
            list<str>: list of html table strings, each defining one service
        """
        html_tables = []
        for _, service in self.services_df.iterrows():
            html_tables.append(self.generate_for_one_service(service))
        return html_tables
    
    def generate_for_one_service(self, service):
        """ generates a single html table string for a single service

        Args:
            service (pd.Series): single service dataframe

        Returns:
            str: single html table string for that service.
        """
        html = ""
        with open(self._table_template_path) as template_file:
            html = template_file.read()
        n = len(html) - 1
        search_index = 0
        while search_index < n:
            found_start_index = html.find("{", search_index)
            found_end_index = html.find("}", search_index)
            if found_start_index == -1 or found_end_index == -1:
                break
            value_to_replace = html[found_start_index:found_end_index+1]
            replace_with_value = service[html[found_start_index+1:found_end_index]]
            html = html.replace(value_to_replace, replace_with_value)
            search_index = found_end_index+1
        return html
    
def generate_html_tables(services_df : pd.DataFrame):
    gen_html = GenerateHTMLTables(services_df)
    return gen_html.generate_for_all_services()


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