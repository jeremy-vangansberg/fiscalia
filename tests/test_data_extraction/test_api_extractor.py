import pytest
from src.data_extraction.api_extractor import APIExtractor
import responses  # Pour mocker les appels API

@pytest.fixture
def api_extractor():
    return APIExtractor(base_url="https://api.test.com", api_key="test_key")

@responses.activate
def test_api_extraction_success(api_extractor):
    """Test l'extraction réussie des données depuis une API"""
    # Prépare la réponse mockée
    responses.add(
        responses.GET,
        "https://api.test.com/endpoint",
        json={"data": "test_data"},
        status=200
    )
    
    # Exécute l'extraction
    data = await api_extractor.extract("endpoint")
    
    # Vérifie les résultats
    assert data["data"] == "test_data"
    assert len(responses.calls) == 1
    assert responses.calls[0].request.headers["Authorization"] == "Bearer test_key"

@responses.activate
def test_api_extraction_error(api_extractor):
    """Test la gestion des erreurs lors de l'extraction"""
    responses.add(
        responses.GET,
        "https://api.test.com/endpoint",
        status=500
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await api_extractor.extract("endpoint")
    
    assert exc_info.value.status_code == 500 