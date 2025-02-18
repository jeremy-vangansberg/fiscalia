import pytest
import os
from pathlib import Path
from src.config.settings import Settings

@pytest.fixture
def env_file(tmp_path):
    """Fixture pour créer un fichier .env de test"""
    env_path = tmp_path / ".env.test"
    env_content = """
LOG_LEVEL=DEBUG
STORAGE_TYPE=local
BOFIP_API_URL=https://test.api/bofip
BOFIP_API_LIMIT=50
API_HOST=127.0.0.1
API_PORT=9000
"""
    env_path.write_text(env_content.strip())
    return env_path

@pytest.fixture(autouse=True)
def clean_env():
    """Nettoie les variables d'environnement avant chaque test"""
    # Sauvegarde les variables existantes
    old_env = dict(os.environ)
    
    # Supprime les variables qui pourraient interférer
    for key in list(os.environ.keys()):
        if key in ["LOG_LEVEL", "STORAGE_TYPE", "BOFIP_API_URL", "BOFIP_API_LIMIT", "API_HOST", "API_PORT"]:
            del os.environ[key]
    
    yield
    
    # Restaure l'environnement
    os.environ.clear()
    os.environ.update(old_env)

def test_default_values():
    """Test les valeurs par défaut des paramètres"""
    settings = Settings(_env_file=None)  # Force aucun fichier .env
    
    assert settings.LOG_LEVEL == "INFO"
    assert settings.STORAGE_TYPE == "local"
    assert settings.API_HOST == "0.0.0.0"
    assert settings.API_PORT == 8000
    assert settings.API_WORKERS == 4
    assert settings.BOFIP_API_LIMIT == 20
    assert settings.BOFIP_API_URL == "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/bofip-impots/records"

def test_data_directories_creation(tmp_path):
    """Test la création automatique des répertoires de données"""
    settings = Settings(_env_file=None, DATA_DIR=tmp_path)
    
    assert settings.DATA_DIR.exists()
    assert settings.RAW_DATA_DIR.exists()
    assert settings.EXTRACTED_DATA_DIR.exists()
    assert settings.PROCESSED_DATA_DIR.exists()
    assert settings.BOFIP_RAW_DIR.exists()
    assert settings.BOFIP_EXTRACTED_DIR.exists()
    assert settings.BOFIP_PROCESSED_DIR.exists()

def test_env_test_override(env_file):
    """Test le chargement des variables depuis .env.test"""
    settings = Settings(_env_file=env_file)
    
    # Vérifie que les valeurs du fichier .env.test sont utilisées
    assert settings.LOG_LEVEL == "DEBUG"
    assert settings.BOFIP_API_URL == "https://test.api/bofip"
    assert settings.BOFIP_API_LIMIT == 50
    assert settings.API_HOST == "127.0.0.1"
    assert settings.API_PORT == 9000

def test_path_resolution():
    """Test la résolution des chemins"""
    settings = Settings(_env_file=None)  # Force aucun fichier .env
    project_root = Path(__file__).parent.parent
    
    assert settings.DATA_DIR == project_root / "data"
    assert settings.RAW_DATA_DIR == project_root / "data/raw"
    assert settings.BOFIP_RAW_DIR == project_root / "data/raw/bofip" 
 