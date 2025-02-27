import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from src.data_extraction.api_extractor import BofipExtractor
from src.storage.base import StorageProvider

@pytest.fixture
def mock_storage():
    """Fixture pour simuler le stockage"""
    storage = Mock(spec=StorageProvider)
    storage.save_file.return_value = str(Path("/fake/path/file.tgz"))
    return storage

@pytest.fixture
def mock_response():
    """Fixture pour simuler la réponse de l'API"""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
        "results": [
            {
                "nom_du_fichier": "bofip_stock_20240201.tgz",
                "telechargement": "https://api.example.com/download/stock.tgz"
            },
            {
                "nom_du_fichier": "bofip_delta_20240201.tgz",
                "telechargement": "https://api.example.com/download/delta.tgz"
            }
        ]
    }
    return mock

@pytest.fixture
def mock_download_response():
    """Fixture pour simuler le téléchargement du fichier"""
    mock = Mock()
    mock.status_code = 200
    mock.content = b"fake_content"
    return mock

class TestBofipExtractor:
    
    @patch("src.data_extraction.api_extractor.get_storage_provider")
    def test_init(self, mock_get_storage, mock_storage):
        """Test l'initialisation de l'extracteur"""
        mock_get_storage.return_value = mock_storage
        extractor = BofipExtractor()
        assert extractor.storage == mock_storage
    
    @patch("requests.get")
    @patch("src.data_extraction.api_extractor.get_storage_provider")
    def test_get_latest_stock_file(self, mock_get_storage, mock_get, mock_storage, mock_response):
        """Test la récupération du dernier fichier stock"""
        mock_get_storage.return_value = mock_storage
        mock_get.return_value = mock_response
        
        extractor = BofipExtractor()
        latest = extractor.get_latest_stock_file()
        
        assert latest["nom_du_fichier"] == "bofip_stock_20240201.tgz"
        assert latest["telechargement"] == "https://api.example.com/download/stock.tgz"
        mock_get.assert_called_once()
    
    @patch("requests.get")
    @patch("src.data_extraction.api_extractor.get_storage_provider")
    def test_download_file(self, mock_get_storage, mock_get, mock_storage, mock_download_response):
        """Test le téléchargement d'un fichier"""
        mock_get_storage.return_value = mock_storage
        mock_get.return_value = mock_download_response
        
        extractor = BofipExtractor()
        file_path = extractor.download_file(
            "https://api.example.com/download/stock.tgz",
            "bofip_stock_20240201.tgz"
        )
        
        mock_storage.save_file.assert_called_once_with(
            b"fake_content",
            "bofip_stock_20240201.tgz"
        )
        assert file_path == str(Path("/fake/path/file.tgz"))
    
    @patch("requests.get")
    def test_api_error(self, mock_get):
        """Test la gestion des erreurs API"""
        mock_get.return_value = Mock(status_code=404)
        
        extractor = BofipExtractor()
        with pytest.raises(Exception):
            extractor.get_latest_stock_file()
    
    @patch("requests.get")
    @patch("src.data_extraction.api_extractor.get_storage_provider")
    def test_no_stock_file(self, mock_get_storage, mock_get, mock_storage):
        """Test le cas où aucun fichier stock n'est trouvé"""
        mock_get_storage.return_value = mock_storage
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response
        
        extractor = BofipExtractor()
        with pytest.raises(ValueError, match="Aucun fichier stock trouvé"):
            extractor.get_latest_stock_file() 