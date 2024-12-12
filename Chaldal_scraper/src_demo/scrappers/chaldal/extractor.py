"""
manage the extraction and data load in supabase
"""
from api_client import ChaldalAPIClient
from repository_services import ChaldalRepositoryServices
class ChaldalExtractor:
    def __init__(self, api_client:ChaldalAPIClient, chaldal_repository: ChaldalRepositoryServices):
        self._api_client = api_client
        self._chaldal_repository = chaldal_repository

    def _call_any_function(self):
        print('Violation of private method')

    def save_extracted_chaldal(self):
        data:bytes = self._api_client.get_data_from_web_site()
        self._chaldal_repository.upload_file_to_supabase(data=data, filename="klk")
