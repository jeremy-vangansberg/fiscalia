from abc import ABC, abstractmethod
from pathlib import Path

class StorageProvider(ABC):
    @abstractmethod
    def save_file(self, file_content: bytes, file_name: str) -> str:
        """Sauvegarde un fichier et retourne son chemin/URI"""
        pass

    @abstractmethod
    def get_file_path(self, file_name: str) -> str:
        """Retourne le chemin/URI complet pour un fichier"""
        pass 