#!/usr/bin/env python
"""
Script de test pour vérifier l'extraction des métadonnées des documents.
"""

import requests
import json
import time
import sys
import os
from pprint import pprint

# Configuration
API_URL = "http://localhost:8000/ask"  # URL de l'API locale

def test_metadata_extraction(question):
    """
    Teste l'extraction des métadonnées avec une question.
    
    Args:
        question (str): La question à poser
    """
    payload = {
        "question": question,
        "include_metadata": True
    }
    
    print(f"\n🔍 Envoi de la question: '{question}'")
    print("📋 Demande spécifique d'inclusion des métadonnées")
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, json=payload)
        
        elapsed = time.time() - start_time
        print(f"⏱️  Temps de réponse: {elapsed:.2f} secondes")
        
        if response.status_code == 200:
            result = response.json()
            
            # Afficher uniquement les métadonnées
            if 'sources' in result and result['sources']:
                print("\n📚 MÉTADONNÉES DES SOURCES:")
                print("=" * 80)
                
                for idx, source in enumerate(result['sources']):
                    print(f"\n[Source {idx+1}]")
                    if isinstance(source, dict):
                        # Afficher l'origine du document
                        print(f"Source: {source.get('source', 'Inconnue')}")
                        
                        # Afficher les métadonnées
                        if 'metadata' in source and source['metadata']:
                            print("Métadonnées:")
                            for key, value in source['metadata'].items():
                                print(f"  - {key}: {value}")
                        else:
                            print("Aucune métadonnée disponible")
                            
                        # Afficher les erreurs éventuelles
                        if 'error' in source:
                            print(f"Erreur: {source['error']}")
                    else:
                        print(f"Format non structuré: {source}")
                
                print("\n" + "=" * 80)
            else:
                print("\n❌ Aucune source retournée")
            
            # Enregistrer la réponse complète
            with open("metadata_response.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print("\n💾 Réponse complète enregistrée dans 'metadata_response.json'")
            
            return result
        else:
            print(f"\n❌ Erreur: Code {response.status_code}")
            print(response.text)
            return None
    
    except Exception as e:
        print(f"\n❌ Exception: {str(e)}")
        return None

if __name__ == "__main__":
    # Si une question est passée en argument, utiliser celle-ci
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        # Sinon utiliser une question par défaut
        question = "Comment fonctionne la TVA en France?"
    
    result = test_metadata_extraction(question)
    
    print("\n🔍 Pour obtenir uniquement les métadonnées des documents, exécutez:")
    print(f"python {os.path.basename(__file__)} \"Votre question ici\"") 