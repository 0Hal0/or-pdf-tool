import pandas as pd

from src.generate_report import generate_report, generate_client_report
from src.generate_html_tables import generate_html_tables
from src.get_services import get_services_from_api, get_services_by_client

def getServicesByName(name, services):
    services = services[services["name"].str.contains(name)]
    return services 

def generic_services_report():
    services_df = get_services_from_api('https://penninelancs.openplace.directory/o/ServiceDirectoryService/v2/services/')
    services_df["telephone"] = services_df["contacts"][0][0]["phones"][0]["number"]
    tables = generate_html_tables(services_df)
    generate_report(tables, "Befriending", "report.pdf")

def service_report_by_client(client, save_data=False):
    services_df = get_services_by_client(client)
    services_df["telephone"] = services_df["contacts"][0][0]["phones"][0]["number"] #Need to learn more about this fix (why is it required)
    try:
        old_services = pd.read_csv(f"resources\\data\\{client}-save.csv")
    except:
        old_services = None
    tables = generate_html_tables(services_df, old_services)
    generate_client_report(tables, client, f"{client}-report.pdf")
    if save_data:
        save_services_data(client, services_df)


def save_services_data(client, services_df):
    services_df.to_csv(f"resources\\data\\{client}-save.csv")

if __name__ == "__main__":
    service_report_by_client("openplace")


