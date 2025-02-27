import tarfile
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Decompressor:
    def __init__(self, output_dir: Path):
        """Initialise le décompresseur
        
        Args:
            output_dir: Répertoire de sortie pour les fichiers décompressés
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Décompresseur initialisé avec le répertoire de sortie: {self.output_dir}")

    def decompress(self, file_path: str) -> Path:
        """Décompresse un fichier tar.gz dans le répertoire de sortie
        
        Args:
            file_path: Chemin du fichier à décompresser
            
        Returns:
            Path: Chemin du répertoire de sortie
            
        Raises:
            tarfile.TarError: Si le fichier est corrompu ou invalide
            OSError: Si une erreur survient lors de la lecture/écriture
        """
        logger.info(f"Décompression du fichier {file_path}")
        try:
            with tarfile.open(file_path, 'r:gz') as tar:
                tar.extractall(path=self.output_dir, filter='data')
                logger.info(f"Fichiers extraits avec succès dans {self.output_dir}")
            return self.output_dir
        except (tarfile.TarError, OSError) as e:
            logger.error(f"Erreur lors de la décompression: {str(e)}")
            raise

# Exemple d'utilisation
if __name__ == "__main__":
    decompressor = Decompressor(output_dir=Path("./extracted_files"))
    decompressor.decompress("./path/to/your/file.tar.gz") 