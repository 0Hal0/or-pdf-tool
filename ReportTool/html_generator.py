import pandas as pd
import os

class HtmlGenerator():

    _table_template_path = os.getcwd() + "\\resources\\html_table_template.html"

    def __init__(self):
        self.something_changed = False
        self.highlight_changes = False
        self.only_changes = False
        return

    def get_replace_value(self, service, column, old_services : pd.DataFrame = None):
        new_value = service[column]
        if old_services is None:
            return new_value
        old_service = old_services.loc[old_services["id"] == service["id"]]
        try:
            if old_service.empty:
                return new_value
            if old_service[column].values[0] == new_value:
                return new_value
        except LookupError as e:
            print(old_service)
            print(f"Could not find last value for {column}")
        self.something_changed = True
        if self.highlight_changes:
            return f"<mark>{new_value}</mark>"
        return new_value

    def generate_for_all_services(self, services : pd.DataFrame, old_services : pd.DataFrame = None, highlight_changes = False, only_changes = False):
        """generates html templates for all services in self.services_df

        Args:
            services (pd.DataFrame): _description_
            old_services (pd.DataFrame, optional): _description_. Defaults to None.

        Returns:
            list<str>: list of html table strings, each defining one service
        """
        self.highlight_changes = highlight_changes
        self.only_changes = only_changes
        html_tables = []
        for _, service in services.iterrows():
            table = self.generate_for_one_service(service, old_services)
            if table:
                html_tables.append(table)
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
        self.something_changed = False
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
        if self.only_changes and not self.something_changed:
            return False
        return html



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