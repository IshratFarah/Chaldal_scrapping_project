"""
manage the extraction and data load in supabase
"""
from api_client import ChaldalAPIClient
from repository_services import ChaldalRepositoryServices
class ChaldalExtractor:
    def __init__(self, api_client: ChaldalAPIClient, chaldal_repository: ChaldalRepositoryServices):
        self._api_client = api_client
        self._chaldal_repository = chaldal_repository

    def save_extracted_data(self):
        self._api_client.get_data_from_web_site()
        self._chaldal_repository.delete_all_files_in_bucket
        self._chaldal_repository.upload_file_to_supabase()
