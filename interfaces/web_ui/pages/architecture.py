import streamlit as st

from components.sidebar import render_sidebar

# Configuration de la page
st.set_page_config(
    page_title="Architecture | Fiscalia",
    page_icon="🏗️",
    layout="wide"
)

render_sidebar(include_examples=False)

# Titre de la page
st.title("🏗️ Architecture de Fiscalia")

# Affichage du diagramme d'architecture
st.image("media/architecture_application.png", caption="Architecture d'application", width=800)

# Explication détaillée des composants
st.markdown("""
### Composants principaux

1. **Interface utilisateur** (Streamlit)
   - Interface web permettant aux utilisateurs de poser des questions et de visualiser les réponses
   - Gestion des exemples de questions prédéfinies

2. **API Backend** (FastAPI)
   - Traitement des requêtes utilisateur
   - Orchestration des différents composants d'intelligence artificielle
   - Gestion du retry pour le démarrage à froid

3. **LangChain**
   - Framework d'orchestration des chaînes d'IA
   - Construction de prompts et gestion des appels aux modèles de langage

4. **Base de connaissances**
   - Vector Store FAISS pour le stockage et la recherche sémantique des documents
   - Contient les données du Code Général des Impôts, BOFIP, et barèmes fiscaux
   - Permet la recherche rapide des documents pertinents pour une question donnée

5. **Modèles d'IA** (Vertex AI)
   - Génération des réponses à partir des documents pertinents
   - Extraction contextuelle des informations
   - Formatage des réponses avec citation des sources

### Flux de traitement d'une question

1. L'utilisateur pose une question via l'interface Streamlit
2. La question est envoyée à l'API FastAPI
3. L'API utilise LangChain pour effectuer une recherche sémantique dans la base de connaissances
4. Les documents pertinents sont récupérés
5. Un prompt est construit avec la question et les documents
6. Le modèle d'IA génère une réponse précise avec citation des sources
7. La réponse est retournée à l'interface utilisateur et affichée avec mise en forme

Cette architecture permet de combiner la puissance des modèles de langage avec une base de connaissances fiable, garantissant des réponses précises et référencées.
""")
