import pytest
from src.database.queries import QueryBuilder, QUERIES
from src.database.models import DataModel

def test_query_builder():
    """Test la construction de requêtes SQL dynamiques"""
    conditions = {
        "source": "test_source",
        "content": "test_content"
    }
    
    query = QueryBuilder.build_select_query("collected_data", conditions)
    
    assert "SELECT * FROM collected_data" in query
    assert "source = %s" in query
    assert "content = %s" in query
    assert "AND" in query

def test_predefined_queries(db_session):
    """Test les requêtes SQL prédéfinies"""
    # Prépare les données de test
    test_data = DataModel(
        source="test_source",
        content="test_content"
    )
    db_session.add(test_data)
    db_session.commit()
    
    # Test la requête recent_data
    result = db_session.execute(QUERIES["select_recent_data"])
    data = result.fetchall()
    assert len(data) > 0
    assert data[0].source == "test_source" 