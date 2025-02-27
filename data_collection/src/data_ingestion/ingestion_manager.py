from typing import List, Dict, Any
from pathlib import Path
from sqlmodel import Session
from datetime import datetime
import logging

from src.models.database import BofipDocument
from src.config.settings import settings
from src.config.database import get_session

logger = logging.getLogger(__name__)

class IngestionManager:
    """Gère le processus d'ingestion des documents BOFiP dans la base de données."""
    
    def __init__(self, batch_size: int = 100):
        """
        Initialise le gestionnaire d'ingestion.
        
        Args:
            batch_size: Nombre de documents à traiter par lot
        """
        self.batch_size = batch_size
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure le logging pour l'ingestion."""
        logging.basicConfig(
            level=settings.LOG_LEVEL,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def process_directory(self, directory: Path) -> Dict[str, int]:
        """
        Traite tous les fichiers d'un répertoire pour ingestion.
        
        Args:
            directory: Chemin du répertoire contenant les fichiers à ingérer
            
        Returns:
            Dict contenant les statistiques d'ingestion
        """
        stats = {"processed": 0, "success": 0, "errors": 0}
        files = list(directory.glob("**/*.xml"))
        
        logger.info(f"Début de l'ingestion - {len(files)} fichiers trouvés")
        
        for i in range(0, len(files), self.batch_size):
            batch = files[i:i + self.batch_size]
            batch_stats = self._process_batch(batch)
            
            for key in stats:
                stats[key] += batch_stats[key]
                
            logger.info(f"Progression: {i + len(batch)}/{len(files)} fichiers traités")
        
        return stats
    
    def _process_batch(self, files: List[Path]) -> Dict[str, int]:
        """
        Traite un lot de fichiers.
        
        Args:
            files: Liste des fichiers à traiter
            
        Returns:
            Dict contenant les statistiques du lot
        """
        stats = {"processed": 0, "success": 0, "errors": 0}
        documents_to_insert = []
        
        for file in files:
            try:
                doc = self._process_file(file)
                if doc:
                    documents_to_insert.append(doc)
                    stats["success"] += 1
            except Exception as e:
                logger.error(f"Erreur lors du traitement de {file}: {str(e)}")
                stats["errors"] += 1
            stats["processed"] += 1
        
        if documents_to_insert:
            self._bulk_insert(documents_to_insert)
        
        return stats
    
    def _process_file(self, file: Path) -> BofipDocument:
        """
        Traite un fichier individuel.
        
        Args:
            file: Chemin du fichier à traiter
            
        Returns:
            Instance de BofipDocument
        """
        # TODO: Implémenter le traitement spécifique des fichiers
        # Cette méthode sera complétée avec le DocumentProcessor
        pass
    
    def _bulk_insert(self, documents: List[BofipDocument]):
        """
        Insère un lot de documents dans la base de données.
        
        Args:
            documents: Liste des documents à insérer
        """
        with Session(get_session()) as session:
            try:
                session.add_all(documents)
                session.commit()
                logger.info(f"{len(documents)} documents insérés avec succès")
            except Exception as e:
                session.rollback()
                logger.error(f"Erreur lors de l'insertion en base: {str(e)}")
                raise 