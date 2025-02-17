import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from src.config.test_settings import TestSettings
import os

settings = TestSettings()

@pytest.fixture(scope="session")
def db_engine():
    """Crée l'engine de base de données pour les tests"""
    database_url = settings.DATABASE_URL
    engine = create_engine(database_url)
    
    # Crée la base de données de test
    Base.metadata.create_all(engine)
    
    yield engine
    
    # Nettoie après les tests
    Base.metadata.drop_all(engine)
    if settings.DATABASE_TYPE == "sqlite":
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