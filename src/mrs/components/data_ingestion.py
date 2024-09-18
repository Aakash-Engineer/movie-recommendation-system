import os
import sys
import requests
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path = 'artifacts/raw/movies.csv'
    raw_data_url = 'https://example.com/movies.csv'


class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()
    
    def start_ingestion(self):
        if not os.path.exists(self.config.raw_data_path):
            self.download_raw_data()
    def download_raw_data(self):
        try:
            response = requests.get(self.config.raw_data_url)
            with open(self.config.raw_data_path, 'wb') as f:
                f.write(response.content)
            print('Raw data downloaded successfully')
        except Exception as e:
            raise Exception(f'Error downloading raw data: {e}')
    