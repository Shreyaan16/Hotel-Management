from configuration.paths_config import (
	CONFIG_PATH,
	TRAIN_FILE_PATH,
	TEST_FILE_PATH,
	PROCESSED_DIR,
	PROCESSED_TRAIN_DATA_PATH,
	PROCESSED_TEST_DATA_PATH,
	MODEL_OUTPUT_PATH,
)
from src.components.data_ingestion import DataIngestion
from src.components.data_preprocessing import DataProcessor
from src.components.model_training import ModelTraining
from src.utils import read_yaml

def run_pipeline() -> None:
	config = read_yaml(CONFIG_PATH)
	if not isinstance(config, dict):
		raise ValueError("Invalid configuration. Please verify configuration/config.yaml")

	ingestion = DataIngestion(config)
	ingestion.run()

	processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
	processor.process()

	trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
	trainer.run()


if __name__ == "__main__":
	run_pipeline()
