import logging
import os
from typing import Any
from dotenv import load_dotenv
import pandas as pd
from sklearn.model_selection import train_test_split
from configuration.paths_config import CONFIG_PATH, RAW_DIR, RAW_FILE_PATH, TEST_FILE_PATH, TRAIN_FILE_PATH
from src.constants import (AZURE_BLOB_NAME, AZURE_CONNECTION_STRING_ENV, AZURE_CONTAINER_NAME, AZURE_STORAGE_CONNECTION_STRING)
from src.utils import read_yaml
from azure.storage.blob import BlobServiceClient 

load_dotenv()

class DataIngestion:
	def __init__(self, config: dict[str, Any]):
		self.config = config["data_ingestion"]
		self.train_test_ratio = self.config["train_ratio"]
		self.container_name = AZURE_CONTAINER_NAME
		self.blob_name = AZURE_BLOB_NAME
		self.connection_string = AZURE_STORAGE_CONNECTION_STRING

		if not self.container_name:
			raise ValueError("AZURE_CONTAINER_NAME is missing in environment")

		if not self.blob_name:
			raise ValueError("AZURE_BLOB_NAME is missing in environment")

		if not self.connection_string:
			raise ValueError(f"Azure connection string is missing. Set environment variable: {AZURE_CONNECTION_STRING_ENV}")

		os.makedirs(RAW_DIR, exist_ok=True)

	def download_csv_from_azure(self) -> None:
		try:
			
			blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
			blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=self.blob_name)

			with open(RAW_FILE_PATH, "wb") as file:
				download_stream = blob_client.download_blob()
				file.write(download_stream.readall())

		except Exception as exc:
			raise RuntimeError("Failed to download CSV from Azure Blob Storage") from exc

	def split_data(self) -> None:
		try:
			data = pd.read_csv(RAW_FILE_PATH)
			train_data, test_data = train_test_split(data, test_size=1 - self.train_test_ratio, random_state=42)
			train_data.to_csv(TRAIN_FILE_PATH, index=False)
			test_data.to_csv(TEST_FILE_PATH, index=False)
		except Exception as exc:
			raise RuntimeError("Failed to split data into train and test sets") from exc

	def run(self) -> None:
		self.download_csv_from_azure()
		self.split_data()

if __name__ == "__main__":
	config = read_yaml(CONFIG_PATH)
	if not isinstance(config, dict):
		raise ValueError("Invalid configuration. Please verify configuration/config.yaml")

	ingestion = DataIngestion(config)
	ingestion.run()
