import requests
import logging
from pathlib import Path
from src.config.settings import settings
from src.data_transformation.storage_handler import LocalStorageHandler, AzureStorageHandler
from io import BytesIO

logger = logging.getLogger(__name__)

class BofipExtractor:
    def __init__(self):
        self.api_url = settings.BOFIP_API_URL
        self.limit = settings.BOFIP_API_LIMIT
        
        # Initialiser le bon handler de stockage
        if settings.STORAGE_TYPE == "azure":
            self.storage_handler = AzureStorageHandler()
        else:
            self.storage_handler = LocalStorageHandler()
        
        logger.info(f"Initialisation BofipExtractor avec URL: {self.api_url}, limite: {self.limit}")
        logger.info(f"Type de stockage: {settings.STORAGE_TYPE}")

    def save_file(self, content: bytes, destination: str) -> str:
        """Sauvegarde le contenu selon le type de stockage configuré"""
        if isinstance(self.storage_handler, AzureStorageHandler):
            try:
                logger.info(f"Début de l'upload Azure pour {destination}")
                logger.info(f"Taille du contenu à uploader: {len(content)} bytes")
                
                # Création du BytesIO
                logger.info("Création du buffer BytesIO")
                data = BytesIO(content)
                
                # Obtention du file client
                logger.info(f"Obtention du file client pour {destination}")
                file_client = self.storage_handler.file_system_client.get_file_client(destination)
                
                # Upload des données
                logger.info("Début de l'upload des données")
                file_client.upload_data(data, overwrite=True)
                logger.info("Upload terminé avec succès")
                
                return destination
                
            except Exception as e:
                logger.error(f"Erreur lors de l'upload Azure: {str(e)}", exc_info=True)
                raise
        else:
            # Sauvegarder en local
            output_path = Path(destination)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(content)
            return str(output_path)

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
            response = requests.get(url)
            response.raise_for_status()
            
            # Construire le chemin de destination
            if isinstance(self.storage_handler, AzureStorageHandler):
                destination = file_name  # Chemin relatif pour Azure
            else:
                destination = str(settings.RAW_DIR / file_name)  # Chemin absolu pour local
            
            file_path = self.save_file(response.content, destination)
            logger.info(f"Fichier sauvegardé à: {file_path}")
                
            return file_path
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction: {str(e)}", exc_info=True)
            raise

    def get_latest_stock_file(self):
        """Récupère les informations du dernier fichier stock disponible"""
        logger.info(f"Requête API: {self.api_url}?limit={self.limit}")
        response = requests.get(f"{self.api_url}?limit={self.limit}")
        
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
    
    def download_file(self, url: str, destination: str) -> str:
        """Télécharge un fichier depuis une URL"""
        logger.info("Téléchargement du fichier...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Utiliser la nouvelle méthode save_file
        return self.save_file(response.content, destination)

