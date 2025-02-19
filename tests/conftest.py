import pytest
import os
import tempfile
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.config.settings import Settings

@pytest.fixture(scope="session")
def test_settings():
    """Fixture pour les paramètres de test"""
    env_path = Path(__file__).parent / ".env.test"
    os.environ["PYTEST_TMPDIR"] = tempfile.mkdtemp()
    return Settings(_env_file=env_path)

@pytest.fixture(scope="session")
def db_engine(test_settings):
    """Crée l'engine de base de données pour les tests"""
    engine = create_engine(test_settings.DATABASE_URL)
    
    # Crée la base de données de test
    SQLModel.metadata.create_all(engine)
    
    yield engine
    
    # Nettoie après les tests
    SQLModel.metadata.drop_all(engine)
    try:
        os.remove("./test.db")
    except FileNotFoundError:
        pass

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Fournit une session de base de données pour chaque test"""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    
    yield session
    
    # Nettoie après chaque test
    session.rollback()
    session.close()

@pytest.fixture(autouse=True)
def setup_test_env(test_settings):
    """Configure l'environnement de test"""
    # Configuration des chemins temporaires
    data_dir = Path(test_settings.DATA_DIR)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    for subdir in ["raw", "extracted", "processed"]:
        (data_dir / subdir).mkdir(parents=True, exist_ok=True)
        (data_dir / subdir / "bofip").mkdir(parents=True, exist_ok=True)
    
    return data_dir

@pytest.fixture
def sample_data():
    """Fournit des données d'exemple pour les tests"""
    return {
        "nom_du_fichier": "bofip_stock_20240201.tgz",
        "telechargement": "https://test.api/bofip/download/stock.tgz",
        "content": b"test content"
    } 