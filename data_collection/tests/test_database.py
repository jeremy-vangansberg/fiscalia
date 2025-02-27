import pytest
from datetime import datetime, date
from src.models.database import BofipDocument
from pydantic import ValidationError
from sqlmodel import select

def test_create_document(session, sample_document):
    """Test la création d'un document dans la base de données."""
    session.add(sample_document)
    session.commit()
    session.refresh(sample_document)
    
    assert sample_document.id is not None
    assert sample_document.document_identifier == "BOI-TEST-000001-20240101"
    assert sample_document.title == "Document de test"

def test_query_document(session, sample_document):
    """Test la recherche d'un document dans la base de données."""
    session.add(sample_document)
    session.commit()
    
    # Recherche par identifiant
    statement = select(BofipDocument).where(
        BofipDocument.document_identifier == "BOI-TEST-000001-20240101"
    )
    doc = session.exec(statement).first()
    
    assert doc is not None
    assert doc.title == "Document de test"
    assert doc.publication_date == date(2024, 1, 1)
    assert doc.document_metadata == {"test_key": "test_value"}

def test_update_document(session, sample_document):
    """Test la mise à jour d'un document dans la base de données."""
    session.add(sample_document)
    session.commit()
    
    # Mise à jour du document
    sample_document.title = "Titre mis à jour"
    session.commit()
    session.refresh(sample_document)
    
    # Vérification de la mise à jour
    assert sample_document.title == "Titre mis à jour"

def test_delete_document(session, sample_document):
    """Test la suppression d'un document dans la base de données."""
    session.add(sample_document)
    session.commit()
    
    # Suppression du document
    session.delete(sample_document)
    session.commit()
    
    # Vérification de la suppression
    statement = select(BofipDocument).where(
        BofipDocument.document_identifier == "BOI-TEST-000001-20240101"
    )
    doc = session.exec(statement).first()
    assert doc is None


def test_metadata_json(session, sample_document):
    """Test le stockage et la récupération des métadonnées JSON."""
    complex_metadata = {
        "sections": ["Section 1", "Section 2"],
        "references": {
            "textes": ["Text 1", "Text 2"],
            "articles": [{"id": 1, "titre": "Article 1"}]
        }
    }
    
    sample_document.document_metadata = complex_metadata
    session.add(sample_document)
    session.commit()
    session.refresh(sample_document)
    
    assert sample_document.document_metadata == complex_metadata
    assert isinstance(sample_document.document_metadata["sections"], list)
    assert isinstance(sample_document.document_metadata["references"], dict) 