import logging
import tarfile
from pathlib import Path

logger = logging.getLogger(__name__)

class Decompressor:
    def __init__(self, output_dir: str):
        """
        Initialise le décompresseur avec un répertoire de sortie.
        
        Args:
            output_dir (str): Chemin du répertoire où extraire les fichiers
        """
        self.output_dir = Path(output_dir)
        logger.info(f"Décompresseur initialisé avec le répertoire de sortie: {self.output_dir}")

    def decompress(self, file_path: str) -> Path:
        """
        Décompresse un fichier .tgz dans le répertoire de sortie.
        
        Args:
            file_path (str): Chemin du fichier à décompresser
            
        Returns:
            Path: Chemin du répertoire contenant les fichiers extraits
        """
        logger.info(f"Décompression du fichier {file_path}")
        
        # Créer le répertoire de sortie s'il n'existe pas
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ouvrir et extraire l'archive
        with tarfile.open(file_path, 'r:gz') as tar:
            # Afficher un résumé du contenu
            members = tar.getmembers()
            logger.info(f"Nombre total de fichiers dans l'archive: {len(members)}")
            
            # Extraire tous les fichiers
            tar.extractall(path=self.output_dir)
            
            # Vérifier l'extraction
            extracted_path = self.output_dir / 'BOFiP'
            if extracted_path.exists():
                logger.info(f"Extraction réussie dans: {extracted_path}")
                logger.info(f"Contenu extrait: {list(extracted_path.iterdir())}")
                return extracted_path
            else:
                logger.error(f"Dossier BOFiP non trouvé dans {self.output_dir}")
                logger.error(f"Contenu du dossier d'extraction: {list(self.output_dir.iterdir())}")
                return self.output_dir

# Exemple d'utilisation
if __name__ == "__main__":
    decompressor = Decompressor(output_dir="./extracted_files")
    decompressor.decompress("./path/to/your/file.tar.gz") 