#!/usr/bin/env python
"""
Script pour inspecter directement les métadonnées stockées dans les index FAISS.
Ce script ouvre les fichiers FAISS et extrait toutes les métadonnées disponibles.
"""

import os
import sys
import json
import pickle
import logging
from typing import Dict, List, Any
import argparse

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("faiss_inspector")

def load_pickle_safely(file_path):
    """Charge un fichier pickle de manière sécurisée"""
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logger.error(f"Erreur lors du chargement du fichier pickle {file_path}: {str(e)}")
        return None

def inspect_faiss_index(base_dir, index_name):
    """Inspecte un index FAISS et extrait ses métadonnées"""
    index_dir = os.path.join(base_dir, index_name)
    
    if not os.path.exists(index_dir):
        logger.error(f"Le répertoire de l'index {index_dir} n'existe pas")
        return
    
    pkl_path = os.path.join(index_dir, "index.pkl")
    faiss_path = os.path.join(index_dir, "index.faiss")
    
    if not os.path.exists(pkl_path) or not os.path.exists(faiss_path):
        logger.error(f"Fichiers d'index manquants dans {index_dir}")
        return
    
    logger.info(f"Chargement de l'index {index_name} depuis {pkl_path}")
    index_data = load_pickle_safely(pkl_path)
    
    if not index_data:
        logger.error(f"Impossible de charger les données de l'index {index_name}")
        return
    
    # Exploration des données de l'index
    logger.info(f"Structure de l'index {index_name}: {type(index_data)}")
    
    # Extraction des métadonnées si disponibles
    metadata = []
    
    try:
        if hasattr(index_data, 'docstore') and hasattr(index_data.docstore, '_dict'):
            logger.info(f"Accès au docstore, {len(index_data.docstore._dict)} documents trouvés")
            
            # Extraction des métadonnées des documents
            for doc_id, doc in index_data.docstore._dict.items():
                doc_info = {
                    "doc_id": str(doc_id),
                    "doc_type": str(type(doc)),
                }
                
                # Extraction du contenu
                if hasattr(doc, 'page_content'):
                    content = doc.page_content
                    doc_info["content_preview"] = content[:200] + '...' if len(content) > 200 else content
                
                # Extraction des métadonnées
                if hasattr(doc, 'metadata'):
                    # Convertir les objets non JSON en chaînes
                    meta_dict = {}
                    for k, v in doc.metadata.items():
                        try:
                            # Test si sérialisable en JSON
                            json.dumps({k: v})
                            meta_dict[k] = v
                        except (TypeError, OverflowError):
                            meta_dict[k] = str(v)
                    
                    doc_info["metadata"] = meta_dict
                
                metadata.append(doc_info)
        else:
            logger.warning(f"Structure d'index non standard pour {index_name}")
            
            # Tentative alternative de récupération des métadonnées
            if isinstance(index_data, dict):
                logger.info(f"Index est un dictionnaire avec {len(index_data)} clés")
                for key, value in index_data.items():
                    logger.info(f"Clé: {key}, Type: {type(value)}")
            
            # Sauvegarde de la structure pour analyse
            with open(f"index_structure_{index_name}.txt", "w") as f:
                f.write(str(index_data)[:10000])
            logger.info(f"Structure de l'index sauvegardée dans index_structure_{index_name}.txt")
    
    except Exception as e:
        logger.error(f"Erreur lors de l'inspection de l'index {index_name}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    
    # Sauvegarde des métadonnées
    if metadata:
        logger.info(f"Extraction de {len(metadata)} documents avec métadonnées")
        output_file = f"metadata_{index_name}_full.json"
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Métadonnées sauvegardées dans {output_file}")
        
        # Affichage des exemples
        print(f"\n==== ÉCHANTILLON DE MÉTADONNÉES POUR {index_name} ====\n")
        for i, doc in enumerate(metadata[:3]):  # Afficher 3 exemples
            print(f"Document {i+1}:")
            if "metadata" in doc:
                print("  Métadonnées:")
                for key, value in doc["metadata"].items():
                    print(f"    {key}: {value}")
            if "content_preview" in doc:
                print(f"  Contenu: {doc['content_preview'][:100]}...")
            print()
        
        return metadata
    else:
        logger.warning(f"Aucune métadonnée trouvée pour {index_name}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Inspecteur de métadonnées FAISS")
    parser.add_argument("--base-dir", default="interfaces/api/app/vector_stores", 
                        help="Répertoire de base contenant les index FAISS")
    parser.add_argument("--index", default=None,
                        help="Nom spécifique de l'index à inspecter (par défaut: tous)")
    
    args = parser.parse_args()
    
    base_dir = args.base_dir
    
    if not os.path.exists(base_dir):
        logger.error(f"Le répertoire de base {base_dir} n'existe pas")
        return
    
    # Liste des index à inspecter
    indexes = []
    if args.index:
        indexes = [args.index]
    else:
        indexes = [d for d in os.listdir(base_dir) 
                  if os.path.isdir(os.path.join(base_dir, d))]
    
    logger.info(f"Inspection des index: {', '.join(indexes)}")
    
    all_metadata = {}
    for index_name in indexes:
        metadata = inspect_faiss_index(base_dir, index_name)
        all_metadata[index_name] = metadata
    
    # Sauvegarde consolidée
    with open("all_metadata_summary.json", "w", encoding="utf-8") as f:
        summary = {
            index: {
                "document_count": len(meta),
                "metadata_keys": list(set().union(*[doc.get("metadata", {}).keys() 
                                                 for doc in meta]))
                                 if meta else []
            }
            for index, meta in all_metadata.items()
        }
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    logger.info("Résumé des métadonnées sauvegardé dans all_metadata_summary.json")
    
    print("\n==== RÉSUMÉ DES MÉTADONNÉES ====\n")
    for index, summary in {
        index: {
            "document_count": len(meta),
            "metadata_keys": list(set().union(*[doc.get("metadata", {}).keys() 
                                             for doc in meta]))
                             if meta else []
        }
        for index, meta in all_metadata.items()
    }.items():
        print(f"Index {index}:")
        print(f"  {summary['document_count']} documents")
        print(f"  Clés de métadonnées: {', '.join(summary['metadata_keys'])}")
        print()

if __name__ == "__main__":
    print("\n🔍 INSPECTEUR DE MÉTADONNÉES FAISS\n")
    main()
    print("\n✅ Inspection terminée\n") 