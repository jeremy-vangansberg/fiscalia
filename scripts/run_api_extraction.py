import logging
from src.data_extraction.api_extractor import BofipExtractor
from src.config.settings import settings

# Configuration avancée du logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def main():
    """Script principal pour l'extraction des données BOFIP"""
    logger.info("Démarrage du processus d'extraction")
    try:
        extractor = BofipExtractor()
        file_path = extractor.extract_data()
        logger.info(f"Extraction terminée avec succès. Fichier sauvegardé : {file_path}")
    except Exception as e:
        logger.error(f"Erreur critique lors de l'extraction des données: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Fin du processus d'extraction")

if __name__ == "__main__":
    main() 