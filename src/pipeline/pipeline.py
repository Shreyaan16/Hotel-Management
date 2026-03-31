from configuration.paths_config import CONFIG_PATH
from src.components.data_ingestion import DataIngestion
from src.utils import read_yaml


def run_pipeline() -> None:
	config = read_yaml(CONFIG_PATH)
	if not isinstance(config, dict):
		raise ValueError("Invalid configuration. Please verify configuration/config.yaml")

	ingestion = DataIngestion(config)
	ingestion.run()


if __name__ == "__main__":
	run_pipeline()