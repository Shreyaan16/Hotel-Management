from configuration.paths_config import (CONFIG_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR)
from src.components.data_ingestion import DataIngestion
from src.components.data_preprocessing import DataProcessor
from src.utils import read_yaml

def run_pipeline() -> None:
	config = read_yaml(CONFIG_PATH)
	if not isinstance(config, dict):
		raise ValueError("Invalid configuration. Please verify configuration/config.yaml")

	ingestion = DataIngestion(config)
	ingestion.run()

	processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
	processor.process()


if __name__ == "__main__":
	run_pipeline()