import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, DataModel
from src.config.test_settings import TestSettings

settings = TestSettings()

@pytest.fixture(scope="function")
def test_db():
    """Crée une base de données SQLite temporaire pour les tests"""
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(engine)

def test_create_data(test_db):
    """Test l'insertion de données"""
    test_data = DataModel(
        source="test_source",
        content="test_content"
    )
    test_db.add(test_data)
    test_db.commit()
    
    result = test_db.query(DataModel).first()
    assert result.source == "test_source"
    assert result.content == "test_content"

def test_data_validation(test_db):
    """Test les contraintes de validation des données"""
    from datetime import datetime
    test_data = DataModel(
        source="test_source",
        content="test_content",
        created_at=datetime.utcnow()
    )
    test_db.add(test_data)
    test_db.commit()
    
    assert test_data.id is not None
    assert isinstance(test_data.created_at, datetime) 