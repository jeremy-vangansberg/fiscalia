from pathlib import Path
from typing import Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

# Obtenir le chemin absolu de la racine du projet
PROJECT_ROOT = Path(__file__).parent.parent.parent

class TestSettings(BaseSettings):
    """Configuration spécifique pour les tests."""
    
    # Configuration du logging
    LOG_LEVEL: str = "DEBUG"

    # Configuration de la base de données de test (SQLite en mémoire)
    DB_URL: str = "sqlite:///./test.db"
    DB_ECHO: bool = True  # Active les logs SQL pour le débogage des tests
    
    # Configuration du stockage
    STORAGE_TYPE: Literal["local", "azure"] = "local"
    
    # Chemins des données de test
    DATA_DIR: Path = PROJECT_ROOT / "tests" / "data"
    RAW_DIR: Path = DATA_DIR / "raw"
    DOCUMENTATION_DIR: Path = DATA_DIR / "documentation"
    EXTRACTED_DIR: Path = DATA_DIR / "extracted"
    
    model_config = SettingsConfigDict(
        env_file=".env.test",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Création automatique des répertoires de test
        for directory in [
            self.DATA_DIR,
            self.RAW_DIR,
            self.DOCUMENTATION_DIR,
            self.EXTRACTED_DIR
        ]:
            directory.mkdir(parents=True, exist_ok=True)

# Instance singleton des settings de test
test_settings = TestSettings() 