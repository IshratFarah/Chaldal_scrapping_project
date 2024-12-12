"""
Crud operations for files and tables
"""
import os
import supabase
from supabase import Client
from api_client import full_filepath
import pandas as pd


class ChaldalRepositoryServices:
    bucket_name = "chaldal_bucket"

    def __init__(self):
        self.client: Client = supabase.create_client(
            supabase_url="https://mfngwnocsedumxuxuotn.supabase.co",
            supabase_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1mbmd3bm9jc2VkdW14dXh1b3RuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxNDcxNDk3NiwiZXhwIjoyMDMwMjkwOTc2fQ.Va3HUp4IumSbyC5Rd4D03D6KFkQvgVg7JjFId5c-dO8"
        )
        self.bucket = self.client.storage.from_(self.bucket_name)

    def delete_all_files_in_bucket(self):
        files = supabase.storage().from_(self.bucket_name).list()
        for file in files:
            supabase.storage().from_(self.bucket_name).remove([file['name']])

    def upload_file_to_supabase(self):
        df: bytes = bytes(pd.read_excel(full_filepath, sheet_name="menu_urls").to_csv().encode('utf-8'))
        # print(type(df))
        self.bucket.upload(path="menu_urls12.xlsx", file=df)
