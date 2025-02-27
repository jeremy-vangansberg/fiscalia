import pytest
import os
import tarfile
from pathlib import Path
from src.data_transformation.decompressor import Decompressor

@pytest.fixture
def temp_dir(tmp_path):
    """Fixture pour créer un répertoire temporaire"""
    return tmp_path

@pytest.fixture
def sample_tar_gz(temp_dir):
    """Fixture pour créer un fichier tar.gz de test"""
    content = b"test content"
    test_file = temp_dir / "test.txt"
    test_file.write_bytes(content)
    
    tar_path = temp_dir / "test.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(test_file, arcname="test.txt")
    
    return tar_path

class TestDecompressor:
    
    def test_init(self, temp_dir):
        """Test l'initialisation du décompresseur"""
        output_dir = temp_dir / "output"
        decompressor = Decompressor(output_dir)
        
        assert decompressor.output_dir == output_dir
        assert output_dir.exists()
    
    def test_decompress_success(self, temp_dir, sample_tar_gz):
        """Test la décompression réussie d'un fichier"""
        output_dir = temp_dir / "output"
        decompressor = Decompressor(output_dir)
        
        result = decompressor.decompress(str(sample_tar_gz))
        
        assert result == output_dir
        assert (output_dir / "test.txt").exists()
        assert (output_dir / "test.txt").read_bytes() == b"test content"
    
    def test_decompress_invalid_file(self, temp_dir):
        """Test la gestion d'un fichier invalide"""
        output_dir = temp_dir / "output"
        decompressor = Decompressor(output_dir)
        
        invalid_file = temp_dir / "invalid.tar.gz"
        invalid_file.write_bytes(b"invalid content")
        
        with pytest.raises(tarfile.TarError):
            decompressor.decompress(str(invalid_file))
    
    def test_decompress_missing_file(self, temp_dir):
        """Test la gestion d'un fichier manquant"""
        output_dir = temp_dir / "output"
        decompressor = Decompressor(output_dir)
        
        with pytest.raises(FileNotFoundError):
            decompressor.decompress(str(temp_dir / "missing.tar.gz"))
    
    def test_decompress_permission_error(self, temp_dir, sample_tar_gz, monkeypatch):
        """Test la gestion des erreurs de permission"""
        output_dir = temp_dir / "output"
        decompressor = Decompressor(output_dir)
        
        def mock_extractall(*args, **kwargs):
            raise PermissionError("Permission denied")
        
        monkeypatch.setattr(tarfile.TarFile, "extractall", mock_extractall)
        
        with pytest.raises(PermissionError):
            decompressor.decompress(str(sample_tar_gz)) 