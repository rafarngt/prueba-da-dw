import pandas as pd
import json
from datetime import datetime

class UtilsFuntions:

    @staticmethod
    def save_file_to_gcs( filename, date, gcs_client, gcs_bucket):
        bucket = gcs_client.get_bucket(gcs_bucket)
        blob = bucket.blob(f'{date}/{filename}')
        blob.upload_from_filename(filename,content_type='text/csv')

    
    @staticmethod
    def save_file_from_io_to_gcs( filename, f, date, gcs_client, gcs_bucket):
        bucket = gcs_client.get_bucket(gcs_bucket)
        blob = bucket.blob(f'{date}/{filename}')
        blob.upload_from_file(f,content_type='text/csv')