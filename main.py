from src.generate_report import generate_report
from src.generate_html_tables import generate_html_tables
from src.get_services import get_services_from_api

if __name__ == "__main__":
    services_df = get_services_from_api('https://penninelancs.openplace.directory/o/ServiceDirectoryService/v2/services/')
    services_df["telephone"] = services_df["contacts"][0][0]["phones"][0]["number"]
    tables = generate_html_tables(services_df)
    generate_report(tables, "Befriending", "report.pdf")