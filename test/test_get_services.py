from src.get_services import get_services_from_api
from unittest import mock
import pandas as pd

class TestGetServices():
    
    def test_get_all_services(self):
        res = get_services_from_api("https://penninelancs.openplace.directory/o/ServiceDirectoryService/v2/services/")
        assert type(res) == pd.DataFrame 
        assert not res.empty