from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Base de données
    DATABASE_TYPE: str = "mysql"
    DATABASE_URL: str = "mysql://user:password@localhost/dbname"
    
    # Scraping
    SCRAPING_LIBRARIES: List[str] = ["requests", "scrapy"]
    
    # API
    API_FRAMEWORK: str = "fastapi"
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "Data Management API"
    API_PREFIX: str = "/api/v1"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

def create_settings():
    """Factory function pour créer les settings"""
    return Settings()

def get_settings():
    """Singleton pattern pour les settings"""
    if not hasattr(get_settings, "_settings"):
        get_settings._settings = create_settings()
    return get_settings._settings

if __name__ == "__main__":
    settings = get_settings()
else:
    settings = get_settings()  # Pour les imports 