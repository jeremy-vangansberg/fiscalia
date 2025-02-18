from src.config.settings import settings
from .local import LocalStorageProvider
from .azure import AzureStorageProvider

def get_storage_provider():
    """Factory pour créer le provider de stockage approprié"""
    if settings.STORAGE_TYPE == "local":
        return LocalStorageProvider(settings.BOFIP_BASE_PATH)
    elif settings.STORAGE_TYPE == "azure":
        if not all([
            settings.AZURE_STORAGE_ACCOUNT,
            settings.AZURE_STORAGE_KEY,
            settings.AZURE_CONTAINER
        ]):
            raise ValueError("Configuration Azure incomplète")
            
        return AzureStorageProvider(
            account_name=settings.AZURE_STORAGE_ACCOUNT,
            account_key=settings.AZURE_STORAGE_KEY,
            container=settings.AZURE_CONTAINER,
            directory=settings.AZURE_DIRECTORY
        )
    else:
        raise ValueError(f"Type de stockage non supporté: {settings.STORAGE_TYPE}") 