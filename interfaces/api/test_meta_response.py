#!/usr/bin/env python
"""
Script de test pour vérifier l'utilisation des métadonnées dans les réponses de l'API.
Ce script pose une question et analyse la façon dont les sources sont citées dans la réponse.
"""

import requests
import json
import time
import sys
import os
import re
from pprint import pprint

# Configuration
API_URL = "http://localhost:8000/ask"  # URL de l'API locale

def extract_citations(text):
    """Extrait les citations de sources dans le texte"""
    # Différents patterns pour extraire les références
    cgi_pattern = r"Article\s+([^,\s]+)\s+du\s+Code\s+Général\s+des\s+Impôts"
    bofip_pattern = r"(TVA\s+-\s+[^(]+)\s+\(BOFIP\s+du\s+([^)]+)\)"
    bareme_pattern = r"(BAREME\s+-\s+[^(]+)\s+\(Barème\s+du\s+([^)]+)\)"
    
    # Recherche des citations
    cgi_refs = re.findall(cgi_pattern, text, re.IGNORECASE)
    bofip_refs = re.findall(bofip_pattern, text, re.IGNORECASE)
    bareme_refs = re.findall(bareme_pattern, text, re.IGNORECASE)
    
    # Combinaison des résultats
    all_refs = {
        "CGI": cgi_refs,
        "BOFIP": bofip_refs,
        "BAREME": bareme_refs
    }
    
    return all_refs

def test_meta_citations(question):
    """
    Teste si l'API utilise correctement les métadonnées dans ses réponses.
    
    Args:
        question (str): La question à poser
    """
    payload = {
        "question": question,
        "include_metadata": True
    }
    
    print(f"\n🔍 Envoi de la question: '{question}'")
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, json=payload)
        
        elapsed = time.time() - start_time
        print(f"⏱️  Temps de réponse: {elapsed:.2f} secondes")
        
        if response.status_code == 200:
            result = response.json()
            
            # Analyse des citations dans la réponse
            answer = result.get("answer", "")
            reasoning = result.get("reasoning", "")
            
            # Extraction et affichage des citations
            answer_citations = extract_citations(answer)
            reasoning_citations = extract_citations(reasoning)
            
            # Affichage des résultats
            print("\n==== ANALYSE DES CITATIONS DANS LA RÉPONSE ====")
            print("\n📝 RÉPONSE:")
            print("-" * 80)
            print(answer)
            print("-" * 80)
            
            print("\n📊 Citations détectées dans la réponse:")
            for source_type, refs in answer_citations.items():
                if refs:
                    print(f"  {source_type}: {', '.join(ref for ref in refs if ref)}")
            
            if not any(refs for refs in answer_citations.values()):
                print("  ❌ Aucune citation détectée - Le modèle utilise probablement encore les numéros de documents")
            
            # Vérification de l'utilisation des numéros de documents
            if re.search(r"Document\s+\d+", answer):
                print("  ⚠️ La réponse contient encore des références par numéro de document")
            
            # Vérification des métadonnées
            print("\n🔎 MÉTADONNÉES DES SOURCES:")
            if 'sources' in result and result['sources']:
                for i, source in enumerate(result['sources'][:3]):  # Limiter à 3 sources pour la lisibilité
                    print(f"\n[Source {i+1}]")
                    if isinstance(source, dict):
                        # Afficher l'origine du document
                        if 'metadata' in source:
                            meta = source['metadata']
                            if 'source' in meta:
                                print(f"Source: {meta['source']}")
                            
                            # Afficher les métadonnées clés
                            key_metadata = ['title', 'title_head', 'title_xml', 'section', 'date']
                            for key in key_metadata:
                                if key in meta:
                                    print(f"{key}: {meta[key]}")
            else:
                print("❌ Aucune métadonnée disponible dans la réponse")
            
            # Enregistrement de la réponse pour analyse
            with open("meta_response_analysis.json", "w", encoding="utf-8") as f:
                json.dump({
                    "answer": answer,
                    "answer_citations": answer_citations,
                    "reasoning": reasoning,
                    "reasoning_citations": reasoning_citations,
                    "sources": result.get("sources", [])
                }, f, ensure_ascii=False, indent=2)
            
            print("\n💾 Analyse complète enregistrée dans 'meta_response_analysis.json'")
            
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
    
    result = test_meta_citations(question)
    
    print("\n✨ CONSEIL:")
    print("Pour obtenir une réponse avec des citations de métadonnées, exécutez:")
    print(f"python {os.path.basename(__file__)} \"Votre question précise sur la TVA ici\"")
    print("\nVérifiez que l'API ne répond plus en utilisant 'Document X' mais avec les métadonnées réelles!") 