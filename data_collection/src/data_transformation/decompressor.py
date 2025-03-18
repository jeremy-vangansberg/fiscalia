import logging
from pathlib import Path
from src.data_transformation.storage_handler import StorageHandler

logger = logging.getLogger(__name__)

class Decompressor:
    def __init__(self, output_dir: str, storage_handler: StorageHandler):
        """
        Initialise le décompresseur avec un répertoire de sortie et un gestionnaire de stockage.
        
        Args:
            output_dir (str): Chemin du répertoire où extraire les fichiers
            storage_handler: Instance de StorageHandler pour gérer le stockage
        """
        self.output_dir = Path(output_dir)

        self.storage_handler = storage_handler

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
        
        extracted_path = self.storage_handler.extract_archive(
            source_path=file_path,
            destination_path=str(self.output_dir)
        )
        
        # Vérifier et logger le résultat
        contents = self.storage_handler.list_directory(str(extracted_path))
        logger.info(f"Contenu extrait dans {extracted_path}: {contents}")
        
        return extracted_path

# Exemple d'utilisation
if __name__ == "__main__":
    decompressor = Decompressor(output_dir="./extracted_files")
    decompressor.decompress("./path/to/your/file.tar.gz") 