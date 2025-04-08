from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag_predictor import answer_question
import time
import sys
import logging
from typing import Dict, Any, List, Optional

# Configuration du logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(sys.stdout),
                        logging.FileHandler('fiscalia_api.log')
                    ])
logger = logging.getLogger(__name__)

# Forcer l'affichage des logs dans le terminal
for handler in logging.getLogger().handlers:
    handler.setLevel(logging.INFO)

print("=== DÉMARRAGE DE L'API FISCALIA ===")
logger.info("Initialisation de l'API Fiscalia")

app = FastAPI(
    title="API Fiscalia",
    description="API pour le chatbot fiscal",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À ajuster pour la production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèle pour les sources détaillées
class SourceDetail(BaseModel):
    index: int
    source: str
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Modèles de données
class QueryRequest(BaseModel):
    question: str
    include_metadata: Optional[bool] = True

class QueryResponse(BaseModel):
    answer: str
    reasoning: str
    sources: Optional[List[Any]] = None
    processing_time: float
    error: Optional[bool] = False

@app.post("/ask", response_model=QueryResponse)
def ask_question(payload: QueryRequest):
    """
    Point d'entrée principal pour répondre aux questions fiscales.
    
    Args:
        payload: Objet contenant la question posée
        
    Returns:
        Un objet contenant la réponse et des métadonnées
    """
    start_time = time.time()
    
    try:
        print(f"📝 Question reçue: {payload.question}")
        logger.info(f"Question reçue: {payload.question}")
        logger.info(f"Inclusion des métadonnées: {payload.include_metadata}")
        
        # Traitement de la question
        logger.info("Appel de answer_question...")
        result = answer_question(payload.question)
        
        processing_time = time.time() - start_time
        
        # Préparation de la réponse
        response = {
            "answer": result["answer"],
            "reasoning": result["reasoning"],
            "processing_time": processing_time,
        }
        
        # Ajout des sources avec métadonnées si demandé
        if "sources" in result:
            if payload.include_metadata:
                # Si inclure les métadonnées complètes
                response["sources"] = result["sources"]
                logger.info(f"Inclus {len(result['sources'])} sources avec métadonnées complètes")
            else:
                # Sinon, inclure uniquement les informations de base
                simple_sources = []
                for source in result["sources"]:
                    if isinstance(source, dict):
                        simple_sources.append(source.get("source", "Source inconnue"))
                    else:
                        simple_sources.append(str(source))
                response["sources"] = simple_sources
                logger.info(f"Inclus {len(simple_sources)} sources simplifiées")
            
        # Indication d'erreur si applicable
        if "error" in result and result["error"]:
            logger.warning(f"Erreur détectée dans la réponse: {result.get('reasoning', 'Raison inconnue')}")
            response["error"] = True
            print(f"❌ Erreur: {result.get('reasoning', 'Raison inconnue')}")
        else:
            print(f"✅ Réponse générée en {processing_time:.2f} secondes")
            
        logger.info(f"Réponse générée en {processing_time:.2f} secondes")
        return response
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Erreur lors du traitement de la question: {str(e)}")
        print(f"❌ Exception: {str(e)}")
        
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return {
            "answer": "Je suis désolé, mais une erreur s'est produite lors du traitement de votre question.",
            "reasoning": f"Erreur technique: {str(e)}",
            "processing_time": processing_time,
            "error": True
        }

@app.get("/health")
def health_check():
    """Endpoint de vérification de santé de l'API"""
    logger.info("Vérification de santé")
    return {"status": "ok"}
