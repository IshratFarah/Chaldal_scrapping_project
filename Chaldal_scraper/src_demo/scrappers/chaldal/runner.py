
from repository_services import ChaldalRepositoryServices
from api_client import ChaldalAPIClient
from extractor import ChaldalExtractor

api_client = ChaldalAPIClient()
repository = ChaldalRepositoryServices()
extractor = ChaldalExtractor(api_client=api_client, chaldal_repository=repository)
extractor.save_extracted_chaldal()
extractor._call_any_function()