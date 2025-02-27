import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from src.data_extraction.api_extractor import BofipExtractor

class TestBofipExtractor:
    
    def test_init(self):
        """Test l'initialisation de l'extracteur"""
        extractor = BofipExtractor()
        assert "bofip-impots" in extractor.base_url
    
    @patch("requests.get")
    def test_get_latest_stock_file(self, mock_get):
        """Test la récupération du dernier fichier stock"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "nom_du_fichier": "bofip_stock_20240201.tgz",
                    "telechargement": "https://api.example.com/download/stock.tgz"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        extractor = BofipExtractor()
        latest = extractor.get_latest_stock_file()
        
        assert "stock" in latest["nom_du_fichier"]
        mock_get.assert_called_once()
    
    @patch("requests.get")
    def test_api_error(self, mock_get):
        """Test la gestion des erreurs API"""
        mock_get.return_value = Mock(status_code=404)
        
        extractor = BofipExtractor()
        with pytest.raises(Exception):
            extractor.get_latest_stock_file() 