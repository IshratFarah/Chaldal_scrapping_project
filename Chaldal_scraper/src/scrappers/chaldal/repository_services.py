"""
Crud operations for files and tables
"""
import os
import supabase
from supabase import create_client, Client
from api_client import full_filepath
import pandas as pd


class ChaldalRepositoryServices:

    def __init__(self, supabase_url=None, supabase_key=None):
        self.client: Client = supabase.create_client(
            supabase_url=os.getenv("SUPABASE_URL"),
            supabase_key=os.getenv("SUPABASE_KEY")
        )
        self.bucket = self.client.storage.from_("chaldal_bucket")

    def upload_file_to_supabase(self):
        df: bytes = bytes(pd.read_excel(full_filepath, sheet_name="menu_urls").to_csv().encode('utf-8'))
        # print(type(df))
        self.bucket.upload(path="menu_urls12.xlsx", file=df)


repository = ChaldalRepositoryServices()
repository.upload_file_to_supabase()

