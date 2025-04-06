#!/usr/bin/env python3
import sys
import logging
from pathlib import Path
import argparse
from datetime import datetime

# Ajouter le chemin du projet au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config.settings import settings
from src.data_ingestion.ingestion_manager import IngestionManager

def setup_logging(log_level: str = "INFO"):
    """Configure le logging pour le script."""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                f"logs/ingestion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            )
        ]
    )

def parse_arguments():
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Script d'ingestion des documents BOFiP dans la base de données"
    )
    
    parser.add_argument(
        "--source-dir",
        type=str,
        help="Répertoire contenant les fichiers à ingérer",
        default=str(settings.EXTRACTED_DIR)
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        help="Nombre de documents à traiter par lot",
        default=100
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Niveau de logging"
    )
    
    return parser.parse_args()

def main():
    """Point d'entrée principal du script."""
    # Parse les arguments
    args = parse_arguments()
    
    # Configure le logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Création du répertoire de logs
        Path("logs").mkdir(exist_ok=True)
        
        # Vérification du répertoire source
        source_dir = Path(args.source_dir)
        if not source_dir.exists():
            raise FileNotFoundError(
                f"Le répertoire source n'existe pas: {source_dir}"
            )
        
        # Initialisation du gestionnaire d'ingestion
        ingestion_manager = IngestionManager(batch_size=args.batch_size)
        
        # Lancement de l'ingestion
        logger.info(f"Début de l'ingestion depuis {source_dir}")
        start_time = datetime.now()
        
        stats = ingestion_manager.process_directory(source_dir)
        
        # Affichage des statistiques
        duration = datetime.now() - start_time
        logger.info("Ingestion terminée")
        logger.info(f"Durée: {duration}")
        logger.info("Statistiques:")
        logger.info(f"  - Documents traités: {stats['processed']}")
        logger.info(f"  - Succès: {stats['success']}")
        logger.info(f"  - Erreurs: {stats['errors']}")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'ingestion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 