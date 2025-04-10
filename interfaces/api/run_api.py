#!/usr/bin/env python
"""
Script de lancement de l'API Fiscalia.
Ce script vérifie l'intégrité des vector stores avant de démarrer l'API.
"""

import os
import sys
import time
import logging
import subprocess
import uvicorn

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('fiscalia_run.log')
    ]
)
logger = logging.getLogger("fiscalia_launcher")

# Bannière de démarrage
banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ████████╗██╗███████╗ ██████╗ █████╗ ██╗     ██╗ █████╗  ║
║   ╚══██╔══╝██║██╔════╝██╔════╝██╔══██╗██║     ██║██╔══██╗ ║
║      ██║   ██║███████╗██║     ███████║██║     ██║███████║ ║
║      ██║   ██║╚════██║██║     ██╔══██║██║     ██║██╔══██║ ║
║      ██║   ██║███████║╚██████╗██║  ██║███████╗██║██║  ██║ ║
║      ╚═╝   ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝ ║
║                                                           ║
║                API Chatbot Fiscal v1.0                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

print(banner)

def check_vector_stores():
    """Vérifie l'intégrité des vector stores"""
    logger.info("Vérification des vector stores...")
    
    base_path = os.path.join(os.path.dirname(__file__), "app", "vector_stores")
    if not os.path.exists(base_path):
        logger.error(f"Répertoire vector_stores introuvable: {base_path}")
        return False
    
    stores = ["cgi", "bofip", "bofip_bareme"]
    missing_stores = []
    
    for store in stores:
        store_path = os.path.join(base_path, store)
        if not os.path.exists(store_path):
            logger.error(f"Vector store {store} introuvable!")
            missing_stores.append(store)
            continue
        
        files = os.listdir(store_path)
        if "index.faiss" not in files or "index.pkl" not in files:
            logger.error(f"Fichiers manquants dans {store}. Trouvés: {files}")
            missing_stores.append(store)
    
    if missing_stores:
        logger.error(f"Vector stores manquants ou incomplets: {missing_stores}")
        return False
    
    logger.info("Tous les vector stores sont présents et complets!")
    return True


def start_api():
    """Démarre l'API Fiscalia"""
    logger.info("Démarrage de l'API Fiscalia...")
    print("🚀 Démarrage de l'API...")
    
    # Configuration de l'API
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    # Démarrage de l'API
    try:
        uvicorn.run("app.main:app", host=host, port=port, reload=False)
    except Exception as e:
        logger.error(f"Erreur lors du démarrage de l'API: {str(e)}")
        print(f"❌ Erreur: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔍 Vérification de l'environnement...")
    logger.info("Lancement du script de démarrage")
    
    # Vérification des variables d'environnement
    required_vars = ["PROJECT_ID", "LOCATION"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Variables d'environnement manquantes: {missing_vars}")
        print(f"❌ Variables d'environnement manquantes: {missing_vars}")
        print("Définissez ces variables avant de démarrer l'API.")
        sys.exit(1)
    
    # Vérification des vector stores
    if not check_vector_stores():
        logger.error("Vérification des vector stores échouée.")
        print("❌ Les vector stores ne sont pas correctement configurés.")
        print("Veuillez vérifier les chemins et les fichiers.")
        choice = input("Voulez-vous continuer quand même? (o/n): ")
        if choice.lower() != 'o':
            sys.exit(1)
    
    # Démarrage de l'API
    print("⏳ Initialisation de l'API...")
    if not start_api():
        logger.error("Échec du démarrage de l'API.")
        sys.exit(1) 