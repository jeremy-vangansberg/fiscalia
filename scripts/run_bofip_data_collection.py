#!/usr/bin/env python3
"""
Script de collecte et de traitement des données du BOFiP (Bulletin Officiel des Finances Publiques).

Ce script fait partie du projet Fiscalia Data Collection et implémente un pipeline modulaire
pour l'extraction, la décompression et la transformation des données fiscales.

Utilisation:
    # Pipeline complet
    python run_bofip_data_collection.py

    # Étapes spécifiques
    python run_bofip_data_collection.py --steps extract decompress
    python run_bofip_data_collection.py --steps transform

Les données sont stockées selon la configuration dans .env (local ou Azure Data Lake Gen2).
"""

import logging
import argparse
from pathlib import Path
from src.data_extraction.api_extractor import BofipExtractor
from src.data_transformation.decompressor import Decompressor
from src.config.settings import settings

# Configuration du logging avec format timestamp pour le suivi
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def extract_data():
    """Étape 1: Extraction des données du BOFiP
    
    Cette étape télécharge le dernier fichier stock disponible depuis l'API BOFiP.
    Le fichier est stocké dans le répertoire configuré (BOFIP_RAW_DIR).
    
    Returns:
        str: Chemin du fichier compressé téléchargé
    """
    logger.info("Début de l'extraction des données BOFiP")
    extractor = BofipExtractor()
    compressed_file_path = extractor.extract_data()
    logger.info(f"Fichier BOFiP extrait : {compressed_file_path}")
    return compressed_file_path

def decompress_data(file_path: str):
    """Étape 2: Décompression des données BOFiP
    
    Décompresse le fichier .tgz téléchargé dans un répertoire dédié.
    
    Args:
        file_path: Chemin du fichier compressé à décompresser
        
    Returns:
        Path: Chemin du répertoire contenant les fichiers décompressés
    """
    logger.info(f"Début de la décompression du fichier : {file_path}")
    decompressor = Decompressor(output_dir=settings.BOFIP_EXTRACTED_DIR)
    extracted_dir = decompressor.decompress(file_path)
    logger.info(f"Fichiers BOFiP décompressés dans : {extracted_dir}")
    return extracted_dir

def transform_data(input_dir: Path):
    """Étape 3: Transformation des données BOFiP
    
    Nettoie et normalise les données extraites pour les préparer au stockage.
    Les données transformées sont stockées dans BOFIP_PROCESSED_DIR.
    
    Args:
        input_dir: Chemin du répertoire contenant les fichiers à transformer
    """
    logger.info(f"Début de la transformation des données dans : {input_dir}")
    # TODO: Implémenter la transformation des données
    # - Nettoyage des données
    # - Normalisation des formats
    # - Validation des schémas
    # - Stockage dans settings.BOFIP_PROCESSED_DIR
    logger.info("Transformation des données terminée")

def run_pipeline(steps=None):
    """Exécute le pipeline de collecte BOFiP
    
    Permet d'exécuter tout ou partie du pipeline de traitement des données.
    Les étapes sont exécutées dans l'ordre : extract -> decompress -> transform.
    
    Args:
        steps: Liste des étapes à exécuter. Si None, exécute tout le pipeline.
               Valeurs possibles: ['extract', 'decompress', 'transform']
    
    Returns:
        Path ou str: Chemin du dernier résultat généré par le pipeline
    """
    try:
        steps = steps or ['extract', 'decompress', 'transform']
        logger.info(f"Démarrage du pipeline BOFiP avec les étapes : {steps}")
        result = None

        if 'extract' in steps:
            result = extract_data()
        
        if 'decompress' in steps and (result or 'extract' not in steps):
            file_to_decompress = result or list(settings.BOFIP_RAW_DIR.glob('*.tgz'))[-1]
            result = decompress_data(str(file_to_decompress))
        
        if 'transform' in steps and (result or 'decompress' not in steps):
            input_dir = result or settings.BOFIP_EXTRACTED_DIR
            transform_data(input_dir)

        logger.info("Pipeline BOFiP terminé avec succès")
        return result

    except Exception as e:
        logger.error(f"Erreur dans le pipeline BOFiP : {str(e)}", exc_info=True)
        raise

def main():
    """Point d'entrée principal du script de collecte BOFiP
    
    Parse les arguments en ligne de commande pour déterminer les étapes à exécuter.
    """
    parser = argparse.ArgumentParser(
        description='Pipeline de collecte et traitement des données BOFiP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--steps',
        nargs='+',
        choices=['extract', 'decompress', 'transform'],
        help='Étapes à exécuter (par défaut: toutes les étapes)'
    )
    
    args = parser.parse_args()
    run_pipeline(args.steps)

if __name__ == "__main__":
    main() 