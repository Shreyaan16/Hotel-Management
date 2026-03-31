import os
from pathlib import Path
from typing import Any, Callable

try:
	from dotenv import load_dotenv as _load_dotenv  # pyright: ignore[reportMissingImports]
except ImportError:
	def _load_dotenv(*args: Any, **kwargs: Any) -> bool:
		return False


load_dotenv: Callable[..., bool] = _load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
AZURE_BLOB_NAME = os.getenv("AZURE_BLOB_NAME")
AZURE_CONNECTION_STRING_ENV = os.getenv("AZURE_CONNECTION_STRING_ENV","AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONNECTION_STRING = os.getenv(AZURE_CONNECTION_STRING_ENV, "")
