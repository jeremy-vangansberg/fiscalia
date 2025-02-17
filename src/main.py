import asyncio
import logging
from pathlib import Path
from data.data_loader import DataLoader
from database.db_manager import DatabaseManager
from config.settings import settings

# Configuration du logging basée sur les paramètres
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

async def process_flat_files():
    """Traite les fichiers plats et les stocke en base de données"""
    try:
        # Initialisation
        data_loader = DataLoader(settings.FLAT_FILES_PATH)
        db_manager = DatabaseManager(settings.DATABASE_URL)
        
        # Création des tables si nécessaire
        db_manager.init_db()
        
        # Traitement des fichiers
        for file_path in Path(settings.FLAT_FILES_PATH).glob('*.csv'):
            logger.info(f"Traitement du fichier: {file_path.name}")
            df = data_loader.load_flat_file(file_path.name)
            
            if data_loader.validate_data(df, settings.DATA_SCHEMA):
                db_manager.store_flat_file_data(df, file_path.name)
                logger.info(f"Fichier {file_path.name} traité avec succès")
            else:
                logger.error(f"Validation échouée pour {file_path.name}")

    except Exception as e:
        logger.error(f"Erreur lors du traitement: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(process_flat_files()) 