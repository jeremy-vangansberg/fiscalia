from typing import Optional, Literal
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Obtenir le chemin absolu de la racine du projet
PROJECT_ROOT = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    # Configuration du logging
    LOG_LEVEL: str = "INFO"

    # Configuration de la base de données
    DATABASE_URL: str = "sqlite:///./data.db"
    
    # Configuration du stockage
    STORAGE_TYPE: Literal["local", "azure"] = "local"
    
    # Chemins des données (local)
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    EXTRACTED_DATA_DIR: Path = DATA_DIR / "extracted"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    
    # Chemins spécifiques BOFiP
    BOFIP_RAW_DIR: Path = RAW_DATA_DIR / "bofip"
    BOFIP_EXTRACTED_DIR: Path = EXTRACTED_DATA_DIR / "bofip"
    BOFIP_PROCESSED_DIR: Path = PROCESSED_DATA_DIR / "bofip"
    
    # Pour Azure Data Lake Gen2
    AZURE_STORAGE_ACCOUNT: Optional[str] = None
    AZURE_STORAGE_KEY: Optional[str] = None
    AZURE_CONTAINER: Optional[str] = None
    AZURE_DIRECTORY: Optional[str] = "bofip"
    
    # Configuration BOFIP API
    BOFIP_API_URL: str = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/bofip-impots/records"
    BOFIP_API_LIMIT: int = 20
    
    # Configuration API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def __init__(self, **kwargs):
        if "_env_file" in kwargs:
            self.model_config["env_file"] = kwargs["_env_file"]
        super().__init__(**kwargs)
        # Création automatique des répertoires de données
        for directory in [
            self.DATA_DIR,
            self.RAW_DATA_DIR,
            self.EXTRACTED_DATA_DIR,
            self.PROCESSED_DATA_DIR,
            self.BOFIP_RAW_DIR,
            self.BOFIP_EXTRACTED_DIR,
            self.BOFIP_PROCESSED_DIR
        ]:
            directory.mkdir(parents=True, exist_ok=True)

# Instance singleton des settings
settings = Settings() 