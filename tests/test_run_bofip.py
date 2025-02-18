import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from scripts.run_bofip_data_collection import (
    extract_data,
    decompress_data,
    transform_data,
    run_pipeline
)

@pytest.fixture
def mock_extractor():
    """Fixture pour simuler l'extracteur"""
    with patch("scripts.run_bofip_data_collection.BofipExtractor") as mock:
        instance = Mock()
        instance.extract_data.return_value = "/fake/path/file.tgz"
        mock.return_value = instance
        yield instance

@pytest.fixture
def mock_decompressor():
    """Fixture pour simuler le décompresseur"""
    with patch("scripts.run_bofip_data_collection.Decompressor") as mock:
        instance = Mock()
        instance.decompress.return_value = Path("/fake/path/extracted")
        mock.return_value = instance
        yield instance

class TestBofipPipeline:
    
    def test_extract_data(self, mock_extractor):
        """Test l'étape d'extraction"""
        result = extract_data()
        
        assert result == "/fake/path/file.tgz"
        mock_extractor.extract_data.assert_called_once()
    
    def test_decompress_data(self, mock_decompressor):
        """Test l'étape de décompression"""
        result = decompress_data("/fake/path/file.tgz")
        
        assert result == Path("/fake/path/extracted")
        mock_decompressor.decompress.assert_called_once_with("/fake/path/file.tgz")
    
    def test_transform_data(self):
        """Test l'étape de transformation"""
        input_dir = Path("/fake/path/extracted")
        # La fonction transform_data ne fait rien pour l'instant
        transform_data(input_dir)
    
    def test_run_pipeline_full(self, mock_extractor, mock_decompressor):
        """Test l'exécution complète du pipeline"""
        result = run_pipeline()
        
        mock_extractor.extract_data.assert_called_once()
        mock_decompressor.decompress.assert_called_once()
        assert result == Path("/fake/path/extracted")
    
    def test_run_pipeline_extract_only(self, mock_extractor, mock_decompressor):
        """Test l'exécution de l'étape d'extraction uniquement"""
        result = run_pipeline(steps=["extract"])
        
        mock_extractor.extract_data.assert_called_once()
        mock_decompressor.decompress.assert_not_called()
        assert result == "/fake/path/file.tgz"
    
    def test_run_pipeline_error(self, mock_extractor):
        """Test la gestion des erreurs dans le pipeline"""
        mock_extractor.extract_data.side_effect = Exception("Test error")
        
        with pytest.raises(Exception, match="Test error"):
            run_pipeline() 