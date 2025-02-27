from azure.storage.filedatalake import DataLakeServiceClient
from .base import StorageProvider
import io

class AzureStorageProvider(StorageProvider):
    def __init__(self, account_name: str, account_key: str, container: str, directory: str):
        self.account_name = account_name
        self.account_key = account_key
        self.container = container
        self.directory = directory
        
        # Initialisation du client Azure
        self.service_client = DataLakeServiceClient(
            account_url=f"https://{account_name}.dfs.core.windows.net",
            credential=account_key
        )
        self.file_system_client = self.service_client.get_file_system_client(container)

    def save_file(self, file_content: bytes, file_name: str) -> str:
        file_path = f"{self.directory}/{file_name}"
        file_client = self.file_system_client.get_file_client(file_path)
        
        # Upload du fichier
        with io.BytesIO(file_content) as data:
            file_client.upload_data(data, overwrite=True)
        
        return f"abfss://{self.container}@{self.account_name}.dfs.core.windows.net/{file_path}"

    def get_file_path(self, file_name: str) -> str:
        return f"abfss://{self.container}@{self.account_name}.dfs.core.windows.net/{self.directory}/{file_name}" 