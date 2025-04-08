from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA, LLMChain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
import sys
import logging
from typing import Dict, List, Any

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('fiscalia_api.log')
    ]
)
logger = logging.getLogger(__name__)

# Forcer l'affichage des logs dans le terminal
for handler in logging.getLogger().handlers:
    handler.setLevel(logging.INFO)

print("=== Démarrage du module rag_predictor ===")
logger.info("Initialisation du module rag_predictor")

# Configuration des chemins
BASE_PATH = os.path.join(os.path.dirname(__file__), "vector_stores")
logger.info(f"Chemin de base pour les vector stores: {BASE_PATH}")

# Chargement des FAISS locaux
def load_vector_stores():
    """Charge tous les vecteurs stores."""
    try:
        logger.info("Début du chargement des vector stores")
        embeddings = VertexAIEmbeddings(
            model_name=os.getenv("MODEL_NAME_EMBEDDING", "text-embedding-004"),
            project=os.getenv("PROJECT_ID"),
            location=os.getenv("LOCATION")
        )
        
        vector_stores = {}
        # Liste des noms de vector stores à charger
        store_names = ["cgi", "bofip", "bofip_bareme"]
        
        # Vérifier que le chemin existe
        if not os.path.exists(BASE_PATH):
            logger.error(f"Le répertoire de base des vector stores n'existe pas: {BASE_PATH}")
            os.makedirs(BASE_PATH, exist_ok=True)
            logger.info(f"Répertoire créé: {BASE_PATH}")
        
        logger.info(f"Contenu du répertoire: {os.listdir(BASE_PATH)}")
        
        for name in store_names:
            try:
                path = os.path.join(BASE_PATH, name)
                if os.path.exists(path):
                    # Vérifier si les fichiers nécessaires existent
                    files = os.listdir(path)
                    logger.info(f"Fichiers trouvés dans {path}: {files}")
                    
                    if "index.faiss" in files and "index.pkl" in files:
                        vector_stores[name] = FAISS.load_local(
                            path,
                            embeddings,
                            allow_dangerous_deserialization=True
                        )
                        logger.info(f"Vector store '{name}' chargé avec succès.")
                    else:
                        logger.error(f"Fichiers index.faiss et/ou index.pkl introuvables dans {path}")
                else:
                    logger.warning(f"Chemin du vector store '{name}' introuvable: {path}")
            except Exception as e:
                logger.error(f"Erreur lors du chargement du vector store '{name}': {str(e)}")
        
        if not vector_stores:
            logger.warning("Aucun vector store chargé!")
            
        return vector_stores
    except Exception as e:
        logger.error(f"Erreur globale lors du chargement des vector stores: {str(e)}")
        return {}

# Initialisation du LLM
def initialize_llm():
    """Initialise le modèle de langage."""
    return VertexAI(
        model_name=os.getenv("MODEL_NAME_LLM", "gemini-1.5-flash"),
        project=os.getenv("PROJECT_ID"),
        location=os.getenv("LOCATION"),
        temperature=float(os.getenv("TEMPERATURE_LLM", "0.1"))
    )

# Prompt pour la génération de réponse
prompt_template = """
Tu es un assistant fiscal expert du Code Général des Impôts et du BOFiP.
Tu dois répondre aux questions de manière claire, structurée et précise EN FRANÇAIS.

La question est : {question}

Utilise les informations des documents suivants pour répondre :
{context}

IMPORTANT: Quand tu cites des sources, NE FAIS PAS RÉFÉRENCE aux documents par leur numéro (ex: "Document 1").
À la place, utilise TOUJOURS les métadonnées disponibles pour citer les sources de manière précise.

Pour les citations de sources, utilise le format Markdown suivant pour les mettre en évidence:
- Pour les sources du CGI: "*<span style='color:#3366CC'>Article [title] du Code Général des Impôts</span>*"
- Pour les sources du BOFIP: "*<span style='color:#339933'>[title_head] (BOFIP du [date])</span>*"
- Pour les barèmes: "*<span style='color:#993399'>[title_head] (Barème du [date])</span>*"

Ce format permettra de mettre en évidence visuellement les sources dans ta réponse.

Si la question nécessite un calcul (par exemple des montants ou des indemnités), explique comment effectuer ce calcul étape par étape.

Si les documents fournis ne contiennent pas suffisamment d'informations pour répondre précisément, indique-le clairement et propose ce que tu sais sur le sujet en précisant que c'est une information générale.

Réponse en français :
"""

# Prompt pour l'explication du raisonnement
reasoning_template = """
Tu es un expert fiscal qui explique son raisonnement.
Tu dois décrire EN FRANÇAIS le processus de réflexion que tu as suivi pour répondre à la question.

La question est : {question}

Les documents consultés contiennent les informations suivantes :
{context}

IMPORTANT: Dans ton raisonnement, cite précisément les sources que tu as utilisées en te basant sur leurs métadonnées.
Utilise également le format Markdown pour mettre en évidence les sources:
- Pour les sources du CGI: "*<span style='color:#3366CC'>Article [title] du Code Général des Impôts, section [section]</span>*"
- Pour les sources du BOFIP: "*<span style='color:#339933'>[title_head] (BOFIP du [date]), section [section]</span>*"
- Pour les barèmes: "*<span style='color:#993399'>[title_head] (Barème du [date]), section [section]</span>*"

Explique ton raisonnement et comment tu es arrivé à cette conclusion, y compris:
- Les sources des informations utilisées avec leurs références précises
- Les éléments clés que tu as identifiés
- Le processus logique suivi pour formuler la réponse

Raisonnement en français :
"""

class FiscalChatbot:
    """Chatbot spécialisé dans la fiscalité française."""
    
    def __init__(self):
        """Initialise le chatbot avec tous les composants nécessaires."""
        self.vector_stores = load_vector_stores()
        self.llm = initialize_llm()
        self.answer_prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["question", "context"]
        )
        self.reasoning_prompt = PromptTemplate(
            template=reasoning_template,
            input_variables=["question", "context"]
        )
        
    def _normalize_documents(self, docs):
        """Normalise les documents pour s'assurer qu'ils ont une structure uniforme."""
        normalized = []
        for doc in docs:
            try:
                if hasattr(doc, 'page_content'):
                    # Déjà au bon format
                    normalized.append(doc)
                elif isinstance(doc, str):
                    # Convertir en objet Document simple
                    from langchain_core.documents import Document
                    normalized.append(Document(page_content=doc, metadata={"source": "Vector Store"}))
                elif isinstance(doc, dict):
                    # Convertir un dict en objet Document
                    from langchain_core.documents import Document
                    page_content = doc.get('page_content', str(doc))
                    metadata = doc.get('metadata', {"source": "Vector Store"})
                    normalized.append(Document(page_content=page_content, metadata=metadata))
                else:
                    # Fallback - convertir en string puis en Document
                    from langchain_core.documents import Document
                    normalized.append(Document(page_content=str(doc), metadata={"source": "Vector Store"}))
                
                logger.info(f"Document normalisé: {type(normalized[-1])}")
                
                # Log détaillé des métadonnées
                if hasattr(normalized[-1], 'metadata'):
                    logger.info(f"Métadonnées: {normalized[-1].metadata}")
                
            except Exception as e:
                logger.error(f"Erreur lors de la normalisation d'un document: {str(e)}")
        
        return normalized
        
    def _retrieve_relevant_documents(self, query: str, k: int = 3) -> List[Any]:
        """Recherche les documents pertinents dans toutes les bases."""
        all_docs = []
        document_metadata = []
        
        try:
            # Vérification que des vector stores sont chargés
            if not self.vector_stores:
                logger.error("Aucun vector store disponible pour la recherche.")
                return []
                
            logger.info(f"Recherche de documents pertinents pour la requête: {query}")
            
            # Recherche dans chaque base et combine les résultats
            for name, store in self.vector_stores.items():
                try:
                    # Tentative d'extraction directe des métadonnées
                    try:
                        logger.info(f"Tentative d'extraction directe des métadonnées pour {name}")
                        # Accéder aux docstore du vectorstore FAISS
                        if hasattr(store, 'docstore') and hasattr(store.docstore, '_dict'):
                            logger.info(f"Accès au docstore de {name}, {len(store.docstore._dict)} documents trouvés")
                            # Extraction des métadonnées brutes
                            raw_metadata = []
                            for doc_id, doc in store.docstore._dict.items():
                                if hasattr(doc, 'metadata'):
                                    raw_metadata.append({
                                        'doc_id': doc_id,
                                        'metadata': doc.metadata,
                                        'content': doc.page_content[:200] + '...' if len(doc.page_content) > 200 else doc.page_content
                                    })
                            logger.info(f"Métadonnées brutes extraites pour {len(raw_metadata)} documents dans {name}")
                            
                            # Sauvegarde des métadonnées pour débuggage
                            import json
                            with open(f"metadata_{name}_raw.json", "w", encoding="utf-8") as f:
                                # Convertir les objets non sérialisables en chaînes
                                simplified_data = []
                                for item in raw_metadata[:10]:  # Limiter à 10 documents pour éviter des fichiers trop volumineux
                                    simplified_item = {
                                        'doc_id': str(item['doc_id']),
                                        'metadata': {k: str(v) for k, v in item['metadata'].items()},
                                        'content': item['content']
                                    }
                                    simplified_data.append(simplified_item)
                                json.dump(simplified_data, f, ensure_ascii=False, indent=2)
                                logger.info(f"Échantillon de métadonnées sauvegardé dans metadata_{name}_raw.json")
                    except Exception as e:
                        logger.error(f"Erreur lors de l'extraction directe des métadonnées de {name}: {str(e)}")
                    
                    # Essayer d'abord avec similarity_search
                    try:
                        logger.info(f"Utilisation de similarity_search pour {name}")
                        docs = store.similarity_search(query, k=k)
                    except Exception as e1:
                        logger.warning(f"similarity_search a échoué pour {name}: {str(e1)}")
                        try:
                            # Essayer avec similarity_search_with_score
                            logger.info(f"Essai avec similarity_search_with_score pour {name}")
                            docs_with_scores = store.similarity_search_with_score(query, k=k)
                            docs = [doc for doc, score in docs_with_scores]
                        except Exception as e2:
                            logger.warning(f"similarity_search_with_score a échoué pour {name}: {str(e2)}")
                            try:
                                # Dernier essai avec similarity_search_by_vector
                                logger.info(f"Essai avec similarity_search_by_vector pour {name}")
                                embedding = store._embedding.embed_query(query)
                                docs = store.similarity_search_by_vector(embedding, k=k)
                            except Exception as e3:
                                logger.error(f"Toutes les méthodes de recherche ont échoué pour {name}: {str(e3)}")
                                docs = []
                    
                    logger.info(f"Documents trouvés dans {name}: {len(docs)}")
                    
                    # Inspecter le premier document pour debug
                    if docs and len(docs) > 0:
                        logger.info(f"Premier document type: {type(docs[0])}")
                        logger.info(f"Premier document contenu: {str(docs[0])[:100]}...")
                        
                        # Extraction avancée des métadonnées
                        for doc in docs:
                            try:
                                # Vérifier et enrichir les métadonnées
                                meta = {}
                                if hasattr(doc, 'metadata'):
                                    meta = doc.metadata.copy() if isinstance(doc.metadata, dict) else {'raw_metadata': str(doc.metadata)}
                                
                                # Ajouter des informations contextuelles
                                meta['source_vectorstore'] = name
                                
                                # Créer une structure enrichie
                                doc_meta = {
                                    'document': doc,
                                    'metadata': meta,
                                    'content_preview': doc.page_content[:100] if hasattr(doc, 'page_content') else str(doc)[:100]
                                }
                                document_metadata.append(doc_meta)
                            except Exception as e:
                                logger.error(f"Erreur lors de l'extraction des métadonnées d'un document: {str(e)}")
                    
                    all_docs.extend(docs)
                except Exception as e:
                    logger.error(f"Erreur lors de la recherche dans {name}: {str(e)}")
            
            logger.info(f"Total de documents trouvés: {len(all_docs)}")
            
            # Normaliser les documents avant de les retourner
            normalized_docs = self._normalize_documents(all_docs)
            logger.info(f"Documents normalisés: {len(normalized_docs)}")
            
            # Attacher les métadonnées enrichies
            self.last_search_metadata = document_metadata
            
            return normalized_docs
        except Exception as e:
            logger.error(f"Erreur dans _retrieve_relevant_documents: {str(e)}")
            self.last_search_metadata = []
            return []
    
    def _format_documents(self, docs: List[Any]) -> str:
        """Formate les documents pour les utiliser dans le prompt."""
        formatted_docs = []
        
        for i, doc in enumerate(docs):
            try:
                # Déterminer le contenu
                if hasattr(doc, 'page_content'):
                    content = doc.page_content
                elif isinstance(doc, str):
                    content = doc
                else:
                    content = str(doc)
                
                # Extraire les métadonnées
                metadata = {}
                if hasattr(doc, 'metadata') and isinstance(doc.metadata, dict):
                    metadata = doc.metadata
                
                # Formater le document avec ses métadonnées
                metadata_str = ""
                if metadata:
                    # Extraire les clés importantes pour la citation
                    source_type = ""
                    if "source" in metadata:
                        if "Code Général des Impôts" in metadata["source"]:
                            source_type = "CGI"
                        elif "Bulletin Officiel des Finances Publiques" in metadata["source"]:
                            source_type = "BOFIP"
                        elif "Barème" in metadata.get("title_head", ""):
                            source_type = "BAREME"
                    
                    # Formater selon le type de source
                    if source_type == "CGI":
                        # Essayer d'extraire des informations plus détaillées pour le CGI
                        title = metadata.get("title", "")
                        section = metadata.get("section", "")
                        
                        # Extraire des informations du contenu si les métadonnées sont insuffisantes
                        if not title or title == "":
                            # Essayer d'extraire un numéro d'article ou une section du contenu
                            import re
                            article_match = re.search(r'Article (\d+[A-Z]?)', content)
                            if article_match:
                                title = article_match.group(1)
                            else:
                                # Utiliser les premiers mots du contenu comme identifiant
                                title_words = content.strip().split()[:3]
                                title = " ".join(title_words) + "..." if title_words else "Non spécifié"
                        
                        # Si aucune section n'est trouvée, essayer d'extraire du contexte
                        if not section or section == "":
                            # Chercher des mots-clés courants dans le CGI
                            for keyword in ["TVA", "impôt sur le revenu", "impôt sur les sociétés", "taxe foncière", "taxe d'habitation"]:
                                if keyword.lower() in content.lower():
                                    section = keyword
                                    break
                            if not section:
                                section = "Disposition générale"
                        
                        metadata_str = f"*<span style='color:#3366CC'>Article {title} du CGI, section '{section}'</span>*"
                    
                    elif source_type == "BOFIP":
                        title = metadata.get("title_head", metadata.get("title_xml", ""))
                        date = metadata.get("date", "")
                        section = metadata.get("section", "")
                        metadata_str = f"*<span style='color:#339933'>{title} (BOFIP du {date})</span>*"
                    
                    elif source_type == "BAREME":
                        title = metadata.get("title_head", metadata.get("title_xml", ""))
                        date = metadata.get("date", "")
                        section = metadata.get("section", "")
                        metadata_str = f"*<span style='color:#993399'>{title} (Barème du {date})</span>*"
                    
                    else:
                        # Format générique si le type n'est pas reconnu
                        metadata_str = f"*<span style='color:#999999'>{metadata.get('source', 'Inconnue')}</span>*"
                
                # Ajouter le document formaté
                formatted_docs.append(f"Document {i+1} {metadata_str}:\n{content}")
            except Exception as e:
                logger.error(f"Erreur lors du formatage du document {i}: {str(e)}")
        
        if not formatted_docs:
            return "Aucun document pertinent trouvé."
            
        return "\n\n".join(formatted_docs)
    
    def generate_answer(self, question: str) -> Dict[str, str]:
        """Génère une réponse et le raisonnement associé à une question."""
        try:
            # Récupération des documents pertinents
            docs = self._retrieve_relevant_documents(question)
            
            if not docs:
                logger.warning(f"Aucun document trouvé pour la question: {question}")
                return {
                    "answer": "Je n'ai pas pu trouver d'informations pertinentes pour répondre à votre question. Pourriez-vous reformuler ou poser une question différente sur la fiscalité française?",
                    "reasoning": "Aucun document pertinent n'a été trouvé dans les bases de données.",
                    "sources": [],
                    "error": False
                }
            
            # Log de debug pour vérifier le format des documents
            logger.info(f"Type du premier document avant formatage: {type(docs[0])}")
            if hasattr(docs[0], 'page_content'):
                logger.info(f"Premier document page_content: {docs[0].page_content[:100]}...")
            else:
                logger.info(f"Premier document sans page_content: {str(docs[0])[:100]}...")
            
            # Extraction des métadonnées détaillées
            detailed_sources = []
            
            # Utiliser les métadonnées enrichies si disponibles
            if hasattr(self, 'last_search_metadata') and self.last_search_metadata:
                logger.info(f"Utilisation des métadonnées enrichies: {len(self.last_search_metadata)} documents")
                
                for i, doc_meta in enumerate(self.last_search_metadata):
                    try:
                        metadata = doc_meta.get('metadata', {})
                        content_preview = doc_meta.get('content_preview', '')
                        
                        # Enrichir les métadonnées pour les sources CGI
                        if 'source' in metadata and "Code Général des Impôts" in metadata['source']:
                            # Essayer d'extraire des informations significatives du contenu
                            import re
                            content = content_preview
                            
                            # Chercher des numéros d'articles
                            article_match = re.search(r'Article (\d+[A-Z]?)', content)
                            if article_match:
                                metadata['article'] = article_match.group(1)
                            
                            # Chercher des sections thématiques
                            for keyword in ["TVA", "impôt sur le revenu", "impôt sur les sociétés", 
                                            "taxe foncière", "IS", "IR", "taxe d'habitation"]:
                                if keyword.lower() in content.lower():
                                    metadata['theme'] = keyword
                                    break
                                    
                            # Extraire quelques mots clés du début du document
                            first_words = " ".join(content.strip().split()[:10]) + "..."
                            metadata['extrait'] = first_words
                        
                        # Formatage des métadonnées
                        source_info = {
                            "index": i + 1,
                            "source": metadata.get('source', 'Document ' + str(i+1)),
                            "metadata": metadata,
                            "content_preview": content_preview
                        }
                        
                        # Filtrer les clés non sérialisables ou trop volumineuses
                        if 'embedding' in source_info['metadata']:
                            del source_info['metadata']['embedding']
                        
                        detailed_sources.append(source_info)
                        logger.info(f"Métadonnées enrichies du document {i+1}: {metadata}")
                        
                    except Exception as e:
                        logger.error(f"Erreur lors de l'extraction des métadonnées enrichies du document {i+1}: {str(e)}")
                        detailed_sources.append({
                            "index": i + 1,
                            "source": "Source inaccessible",
                            "error": str(e)
                        })
            else:
                # Fallback sur l'extraction classique
                logger.info("Utilisation de l'extraction de métadonnées standard")
                
                for i, doc in enumerate(docs):
                    try:
                        metadata = {}
                        if hasattr(doc, 'metadata') and isinstance(doc.metadata, dict):
                            metadata = doc.metadata
                            
                        # Formatage des métadonnées
                        source_info = {
                            "index": i + 1,
                            "source": metadata.get('source', 'Document ' + str(i+1)),
                            "metadata": metadata
                        }
                        
                        # Filtrer les clés non sérialisables ou trop volumineuses
                        if 'embedding' in source_info['metadata']:
                            del source_info['metadata']['embedding']
                        
                        detailed_sources.append(source_info)
                        logger.info(f"Métadonnées du document {i+1}: {metadata}")
                        
                    except Exception as e:
                        logger.error(f"Erreur lors de l'extraction des métadonnées du document {i+1}: {str(e)}")
                        detailed_sources.append({
                            "index": i + 1,
                            "source": "Source inaccessible",
                            "error": str(e)
                        })
            
            # Conversion directe en texte pour éviter les problèmes d'attributs
            context = self._format_documents(docs)
            logger.info(f"Contexte formaté: {len(context)} caractères")
            
            try:
                # Méthode alternative sans create_stuff_documents_chain
                answer_chain = LLMChain(
                    llm=self.llm,
                    prompt=self.answer_prompt
                )
                
                reasoning_chain = LLMChain(
                    llm=self.llm,
                    prompt=self.reasoning_prompt
                )
                
                # Exécution des chaînes avec des variables simples
                logger.info("Génération de la réponse avec LLMChain...")
                answer_result = answer_chain.invoke({
                    "question": question,
                    "context": context
                })
                answer = answer_result.get("text", "")
                logger.info(f"Réponse générée: {len(answer)} caractères")
                
                logger.info("Génération du raisonnement avec LLMChain...")
                reasoning_result = reasoning_chain.invoke({
                    "question": question,
                    "context": context
                })
                reasoning = reasoning_result.get("text", "")
                logger.info(f"Raisonnement généré: {len(reasoning)} caractères")
                
            except Exception as e:
                logger.error(f"Erreur lors de l'utilisation de LLMChain: {str(e)}")
                logger.info("Tentative avec appel direct au LLM...")
                
                # Si tout échoue, utiliser le LLM directement
                combined_prompt = f"""
                Question: {question}
                
                Contexte: {context[:4000]}... (tronqué pour la longueur)
                
                Réponse:
                """
                
                answer = self.llm.invoke(combined_prompt)
                reasoning = f"Raisonnement simplifié en raison d'une erreur technique. La réponse a été générée directement à partir du contexte."
            
            logger.info(f"Réponse complétée avec {len(detailed_sources)} sources détaillées")
            return {
                "answer": answer,
                "reasoning": reasoning,
                "sources": detailed_sources
            }
            
        except Exception as e:
            # Gestion des erreurs pour assurer la robustesse
            error_message = f"Une erreur s'est produite: {str(e)}"
            logger.error(error_message)
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "answer": "Je suis désolé, mais je ne peux pas répondre à cette question pour le moment en raison d'une erreur technique.",
                "reasoning": error_message,
                "error": True
            }

# Initialisation d'une instance unique du chatbot
chatbot = FiscalChatbot()

def answer_question(query: str) -> Dict[str, Any]:
    """Point d'entrée pour répondre aux questions."""
    return chatbot.generate_answer(query)

