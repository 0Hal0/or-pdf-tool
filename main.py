from src.generate_report import generate_report, generate_report_with_header
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

def service_report_by_client(client):
    services_df = get_services_by_client(client)
    services_df["telephone"] = services_df["contacts"][0][0]["phones"][0]["number"] #Need to learn more about this fix (why is it required)
    tables = generate_html_tables(services_df)
    generate_report_with_header(tables, client, f"{client}-report.pdf")

if __name__ == "__main__":
    service_report_by_client("openplace")


