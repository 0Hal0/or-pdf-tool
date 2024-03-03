import os
from .service_manager import ServiceManager
from .html_generator import HtmlGenerator
from .pdf_generator import PdfGenerator
def generate_user_report(include_history : bool, save_to_history : bool, only_changes : bool, user : str):
    service_manager = ServiceManager()
    html_gen = HtmlGenerator()
    pdf_gen = PdfGenerator()

    old_services_df = service_manager.try_get_last_services(user) if include_history else None
    services_df = service_manager.get_services_for_user(user)
    if save_to_history:
        service_manager.save_services(services_df, user)
    html_tables = html_gen.generate_for_all_services(services_df, old_services_df)
    save_path = f"{user}-services.pdf"
    pdf_gen.create_report(html_tables, save_path)
    return os.path.join(os.getcwd(), save_path)

def get_services_for_user(user : str):
    return ServiceManager().try_get_last_services(user)


    
    
