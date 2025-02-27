import pytest
import os
import tempfile
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
from src.config.test_settings import TestSettings
from src.models.database import BofipDocument
from datetime import datetime, date
import datetime as dt

@pytest.fixture(scope="session")
def test_settings():
    """Fixture pour les paramètres de test"""
    env_path = Path(__file__).parent / ".env.test"
    os.environ["PYTEST_TMPDIR"] = tempfile.mkdtemp()
    return TestSettings(_env_file=env_path)

@pytest.fixture(scope="session")
def db_engine(test_settings):
    """Crée l'engine de base de données pour les tests"""
    engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False}  # Nécessaire pour SQLite
    )
    
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
    data_dir = Path(os.environ["PYTEST_TMPDIR"]) / "data"
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

@pytest.fixture(name="session")
def session_fixture(db_engine):
    """Fixture qui fournit une session de base de données de test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(name="sample_document")
def sample_document_fixture():
    """Fixture qui fournit un exemple de document BOFiP pour les tests."""
    return BofipDocument(
        document_identifier="BOI-TEST-000001-20240101",
        title="Document de test",
        publication_date=date(2024, 1, 1),
        creator="Test Author",
        publisher="Direction Générale des Finances Publiques",
        language="fr",
        format="text/html",
        contenu_type="TEST",
        file_path="/test/path",
        data_html_file="data.html",
        document_xml_file="document.xml",
        html_content="<p>Contenu de test</p>",
        document_metadata={"test_key": "test_value"},
        date_import=datetime.now(dt.UTC)
    ) 