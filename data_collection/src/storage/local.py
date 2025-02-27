import os
from pathlib import Path
from .base import StorageProvider

class LocalStorageProvider(StorageProvider):
    def __init__(self, base_path: Path):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save_file(self, file_content: bytes, file_name: str) -> str:
        file_path = self.get_file_path(file_name)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        return str(file_path)

    def get_file_path(self, file_name: str) -> str:
        return str(self.base_path / file_name) 