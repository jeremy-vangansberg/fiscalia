#!/usr/bin/env python
"""
Script de test pour l'API Fiscalia.
Exécuter ce script pour tester l'API avec une question simple.
"""

import requests
import json
import time
import sys
import os

# Configuration
API_URL = "http://localhost:8000/ask"  # URL de l'API locale

def test_api(question):
    """
    Teste l'API avec une question.
    
    Args:
        question (str): La question à poser
        
    Returns:
        dict: La réponse de l'API
    """
    payload = {"question": question}
    
    print(f"\n🔍 Envoi de la question: '{question}'")
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, json=payload)
        
        elapsed = time.time() - start_time
        print(f"⏱️  Temps de réponse: {elapsed:.2f} secondes")
        
        if response.status_code == 200:
            result = response.json()
            
            # Affichage de la réponse
            print("\n✅ Réponse reçue:")
            print(f"\n🤖 Réponse: {result['answer']}")
            print(f"\n🧠 Raisonnement: {result['reasoning']}")
            
            if 'sources' in result and result['sources']:
                print("\n📚 Sources:")
                for src in result['sources']:
                    print(f"  - {src}")
            
            if 'error' in result and result['error']:
                print("\n⚠️ ERREUR DÉTECTÉE DANS LA RÉPONSE")
            
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
    
    result = test_api(question)
    
    # Enregistrement de la réponse dans un fichier JSON pour référence
    if result:
        with open("derniere_reponse.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("\n💾 Réponse enregistrée dans 'derniere_reponse.json'") 