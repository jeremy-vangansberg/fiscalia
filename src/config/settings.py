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
    # Pour le stockage local
    BOFIP_BASE_PATH: Path = PROJECT_ROOT / "data" / "bofip"
    # Pour Azure Data Lake Gen2
    AZURE_STORAGE_ACCOUNT: Optional[str] = None
    AZURE_STORAGE_KEY: Optional[str] = None
    AZURE_CONTAINER: Optional[str] = None
    AZURE_DIRECTORY: Optional[str] = "bofip"
    
    # Configuration BOFIP API
    BOFIP_API_URL: str
    BOFIP_API_LIMIT: int = 20
    
    # Configuration API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    
    # Configuration du modèle
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

# Instance singleton des settings
settings = Settings() 