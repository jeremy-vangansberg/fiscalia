import pytest
from datetime import datetime
from src.database.models import FlatFileData

@pytest.fixture
def sample_flat_file():
    """Fixture pour créer un exemple de fichier plat"""
    return {
        "filename": "bofip_stock_20240201.tgz",
        "content": "contenu du fichier...",
        "source_type": "bofip_api",
        "status": "raw"
    }

def test_create_flat_file_data(sample_flat_file):
    """Test la création d'un modèle FlatFileData"""
    data = FlatFileData(
        filename=sample_flat_file["filename"],
        content=sample_flat_file["content"],
        source_type=sample_flat_file["source_type"]
    )
    
    assert data.filename == sample_flat_file["filename"]
    assert data.content == sample_flat_file["content"]
    assert data.source_type == sample_flat_file["source_type"]
    assert data.status == "raw"  # valeur par défaut
    assert isinstance(data.processed_at, datetime)

def test_flat_file_data_defaults():
    """Test les valeurs par défaut du modèle FlatFileData"""
    data = FlatFileData(
        filename="test.tgz",
        content="test content"
    )
    
    assert data.filename == "test.tgz"
    assert data.content == "test content"
    assert data.source_type is None  # optionnel
    assert data.status == "raw"  # valeur par défaut
    assert isinstance(data.processed_at, datetime) 