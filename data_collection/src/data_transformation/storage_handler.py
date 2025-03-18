from abc import ABC, abstractmethod
from pathlib import Path
import tarfile
import logging
from azure.storage.filedatalake import DataLakeServiceClient
from io import BytesIO
from src.config.settings import settings
from azure.core.exceptions import AzureError

logger = logging.getLogger(__name__)

class StorageHandler(ABC):
    """Interface abstraite pour gérer différents types de stockage"""
    
    @abstractmethod
    def extract_archive(self, source_path: str, destination_path: str) -> Path:
        """Extrait une archive vers la destination"""
        pass

    @abstractmethod
    def list_directory(self, path: str) -> list:
        """Liste le contenu d'un répertoire"""
        pass

class LocalStorageHandler(StorageHandler):
    """Gestionnaire pour le stockage local"""
    
    def extract_archive(self, source_path: str, destination_path: str) -> Path:
        output_dir = Path(destination_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with tarfile.open(source_path, 'r:gz') as tar:
            tar.extractall(path=output_dir)
            
        extracted_path = output_dir / 'BOFiP'
        if not extracted_path.exists():
            logger.error(f"Extraction locale échouée: {output_dir}")
            return output_dir
        return extracted_path

    def list_directory(self, path: str) -> list:
        return list(Path(path).iterdir())

class AzureStorageHandler(StorageHandler):
    """Gestionnaire pour Azure Data Lake Storage"""
    
    def __init__(self, connection_string: str = None, container_name: str = None):
        try:
            logger.info("Initialisation du AzureStorageHandler")
            # Utiliser l'URL et la clé d'accès
            account_url = f"https://{settings.AZURE_STORAGE_ACCOUNT}.dfs.core.windows.net"
            logger.info(f"URL du compte: {account_url}")
            
            logger.info("Création du service client")
            self.service_client = DataLakeServiceClient(
                account_url=account_url,
                credential=settings.AZURE_STORAGE_KEY
            )
            
            self.container_name = settings.AZURE_CONTAINER
            logger.info(f"Nom du container: {self.container_name}")
            
            logger.info("Obtention du file system client")
            self.file_system_client = self.service_client.get_file_system_client(self.container_name)
            logger.info("AzureStorageHandler initialisé avec succès")
            
        except AzureError as e:
            logger.error(f"Erreur d'initialisation Azure: {str(e)}", exc_info=True)
            raise

    def extract_archive(self, source_path: str, destination_path: str) -> Path:
        # Lire l'archive depuis Azure
        source_file = self.file_system_client.get_file_client(source_path)
        archive_data = source_file.download_file().readall()
        
        # Extraire en mémoire
        with BytesIO(archive_data) as bio:
            with tarfile.open(fileobj=bio, mode='r:gz') as tar:
                # Extraire chaque fichier vers Azure
                for member in tar.getmembers():
                    if member.isfile():
                        file_content = tar.extractfile(member).read()
                        azure_path = f"{destination_path}/{member.name}"
                        file_client = self.file_system_client.get_file_client(azure_path)
                        file_client.upload_data(file_content, overwrite=True)
        
        return Path(f"{destination_path}/BOFiP")

    def list_directory(self, path: str) -> list:
        paths = []
        directory_client = self.file_system_client.get_directory_client(path)
        paths_iter = directory_client.get_paths()
        return [p.name for p in paths_iter] 