from extractor import *

api_client = ChaldalAPIClient()
repository = ChaldalRepositoryServices()
extractor = ChaldalExtractor(api_client=api_client, chaldal_repository=repository)
extractor.save_extracted_data()
