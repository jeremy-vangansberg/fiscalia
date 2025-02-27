import requests
import logging
from src.config.settings import settings
from src.storage import get_storage_provider

logger = logging.getLogger(__name__)

class BofipExtractor:
    def __init__(self):
        self.base_url = settings.BOFIP_API_URL
        self.limit = settings.BOFIP_API_LIMIT
        self.storage = get_storage_provider()
        logger.info(f"Initialisation BofipExtractor avec URL: {self.base_url}, limite: {self.limit}")
        logger.info(f"Type de stockage: {settings.STORAGE_TYPE}")

    def extract_data(self):
        """Exécute l'extraction complète des données"""
        try:
            logger.info("Début de l'extraction des données")
            
            # Récupération du dernier fichier stock
            logger.info("Recherche du dernier fichier stock disponible...")
            latest_file = self.get_latest_stock_file()
            file_name = latest_file['nom_du_fichier']
            url = latest_file['telechargement']
            logger.info(f"Fichier trouvé - Nom: {file_name}")
            logger.info(f"URL de téléchargement: {url}")
            
            # Téléchargement et sauvegarde du fichier
            logger.info("Début du téléchargement...")
            file_path = self.download_file(url, file_name)
            logger.info(f"Fichier sauvegardé à: {file_path}")
                
            return file_path
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction: {str(e)}", exc_info=True)
            raise

    def get_latest_stock_file(self):
        """Récupère les informations du dernier fichier stock disponible"""
        logger.info(f"Requête API: {self.base_url}?limit={self.limit}")
        response = requests.get(f"{self.base_url}?limit={self.limit}")
        
        if response.status_code != 200:
            logger.error(f"Erreur API: Status {response.status_code}")
            logger.error(f"Réponse: {response.text}")
            response.raise_for_status()
            
        response_json = response.json()
        logger.info(f"Nombre total de résultats: {len(response_json.get('results', []))}")
        
        stock_files = [x for x in response_json['results'] 
                      if x['telechargement'].rfind('stock') != -1]
        logger.info(f"Nombre de fichiers stock trouvés: {len(stock_files)}")
        
        if not stock_files:
            logger.error("Aucun fichier stock trouvé dans la réponse API")
            raise ValueError("Aucun fichier stock trouvé")
            
        latest = stock_files[0]
        logger.info(f"Dernier fichier stock: {latest.get('nom_du_fichier', 'nom inconnu')}")
        return latest
    
    def download_file(self, url, file_name):
        """Télécharge le fichier depuis l'URL donnée et le sauvegarde"""
        try:
            logger.info("Téléchargement du fichier...")
            response = requests.get(url)
            response.raise_for_status()
            
            # Utilisation du provider de stockage pour sauvegarder le fichier
            file_path = self.storage.save_file(response.content, file_name)
            logger.info(f"Fichier sauvegardé avec succès: {file_path}")
            
            return file_path
            
        except Exception as e:
            logger.error(f"Erreur pendant le téléchargement: {str(e)}", exc_info=True)
            raise 

