import pdfkit

class GenerateReport():

    _report = '<link rel="stylesheet" href="style.css"> \n<body>'
    _report_end = "\n</body>"
    _path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    def __init__(self):
        with open("resources\\report_template.html") as template:
            self.report = template
        return
    
    def create_service_type_report(self, service_tables, service_type, file_path=None):
        self._report += f'\n<br>\n<h1>Service Type: {service_type}</h1>'
        index = 0
        for table in service_tables:
            self._report += '\n'
            self._report += table
            if index > 1:
                self._report += '<br><br><br>\n'
            index +=  1
    
        report = self._report + self._report_end

        if file_path != None:
            self.save_html_report_as_pdf(report, file_path)
        return report
    
    def save_html_report_as_pdf(self, report, file_path='out.pdf'):
        with open("resources\\temp_html_report.html", "w") as html_file:
            html_file.write(report)
        config = pdfkit.configuration(wkhtmltopdf=self._path_wkhtmltopdf)
        pdfkit.from_file("resources\\temp_html_report.html", file_path, configuration=config, options={"enable-local-file-access": ""})
        #pdfkit.from_string(report, file_path, css='resources\\style.css', configuration=config, options={"enable-local-file-access": ""})
        return
    

def generate_report(service_tables : list[str], service_type=None, file_path=None):
    report_generator = GenerateReport()
    if service_type != None:
        report_generator.create_service_type_report(service_tables, service_type, file_path)