import streamlit as st
import os 
import time
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import requests

# Configuration
API_URL = os.getenv("API_URL", "http://api:8080/ask")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "10"))
DEBUG = os.getenv("DEBUG", None)
USE_AUTH = os.getenv("USE_AUTH", "false").lower() == "true"

def call_private_api(question, API_URL, timeout):
    headers = {}

    if USE_AUTH:
        from google.auth.transport.requests import Request
        from google.oauth2 import id_token
        token = id_token.fetch_id_token(Request(), API_URL)
        headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(API_URL, headers=headers, json={"question": question}, timeout=timeout)
    return response

# Configuration de la page
st.set_page_config(
    page_title="Fiscalia",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS minimal pour colorer les sources uniquement
st.markdown("""
<style>
/* Style pour les sources colorées */
span[style*="color"] {
    display: inline-block;
    padding: 2px 5px;
    border-radius: 3px;
    background-color: rgba(0,0,0,0.05);
    margin: 0 2px;
}
</style>
""", unsafe_allow_html=True)

# Définition des exemples de questions
EXAMPLE_QUESTIONS = [
    {
        "title": "TVA", 
        "description": "Comment fonctionne la TVA en France?",
        "category": "Taxe sur la valeur ajoutée"
    },
    {
        "title": "Impôt sur le revenu", 
        "description": "Quel est le barème de l'impôt sur le revenu pour 2024?",
        "category": "Impôts des particuliers"
    },
    {
        "title": "Indemnités kilométriques", 
        "description": "Comment calculer les indemnités kilométriques pour une voiture de 6CV?",
        "category": "Frais professionnels"
    },
    {
        "title": "Micro-entreprise", 
        "description": "Quelles sont les charges sociales pour une micro-entreprise?",
        "category": "Entrepreneuriat"
    },
]

# Fonction pour définir la question à poser
def set_question(question):
    st.session_state.question_to_ask = question

# Panneau latéral (Sidebar)
with st.sidebar:
    st.markdown("<h1>Fiscalia</h1>", unsafe_allow_html=True)
    
    # Navigation
    st.subheader("Navigation")
    st.page_link("app.py", label="💬 Assistant fiscal", icon="📝")
    st.page_link("pages/architecture.py", label="🏗️ Architecture", icon="🔍")
    
    # Exemples de questions
    st.subheader("Exemples de questions")
    
    # Afficher les exemples de questions avec des boutons Streamlit
    for i, example in enumerate(EXAMPLE_QUESTIONS):
        # Utiliser directement la description de la question comme texte du bouton
        st.button(example['description'], key=f"btn_{i}", on_click=set_question, args=(example['description'],))
        st.markdown("---")
    
    # Section À propos
    st.subheader("À propos")
    st.markdown("""
    **Fiscalia** est un assistant fiscal intelligent basé sur l'IA qui vous aide à naviguer dans la complexité de la fiscalité française.
    
    Notre base de connaissances inclut :
    - Le Code Général des Impôts
    - Le Bulletin Officiel des Finances Publiques (BOFiP)
    - Les barèmes fiscaux actualisés
    """)
    
    # Informations légales
    st.subheader("Informations légales")
    with st.expander("Mentions légales"):
        st.write("""
        Les réponses fournies par cet assistant sont données à titre informatif uniquement et ne constituent pas un conseil fiscal professionnel. 
        
        Consultez un expert-comptable ou un conseiller fiscal pour des conseils adaptés à votre situation personnelle.
        
        Fiscalia peut parfois se tromper ou donner des informations incomplètes. Vérifiez toujours les informations importantes auprès des sources officielles.
        
        © 2024 Fiscalia. Tous droits réservés.
        """)

# Contenu principal - Chatbot
# Initialisation de l'historique des messages s'il n'existe pas
if "messages" not in st.session_state:
    st.session_state.messages = []

# Si aucun message, afficher un message d'accueil
if not st.session_state.messages:
    st.title("💬 Fiscalia")
    st.write("Posez vos questions sur la fiscalité française et obtenez des réponses précises basées sur les textes officiels.")

# Affiche l'historique des messages avec le style par défaut de Streamlit
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    st.chat_message(role).markdown(content, unsafe_allow_html=True)

# Toujours afficher le champ de saisie
question_from_input = st.chat_input("Posez votre question fiscale ici...")

# Si une question a été sélectionnée depuis les exemples, elle est prioritaire
if "question_to_ask" in st.session_state and st.session_state.question_to_ask:
    question = st.session_state.question_to_ask
    st.session_state.question_to_ask = None  # Effacer la question après utilisation
elif question_from_input:  # Sinon, utiliser l'entrée manuelle si disponible
    question = question_from_input
else:
    question = None  # Aucune question à traiter

# Traitement des questions
if question:
    # Affiche la question
    st.chat_message("user").markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Appelle l'API avec retry
    with st.spinner("Recherche en cours..."):
        retry_count = 0
        success = False
        error_message = None
        
        # Conteneur pour afficher les messages de statut
        status_container = st.empty()
        
        while retry_count < MAX_RETRIES and not success:
            try:
                if retry_count > 0:
                    # Informer l'utilisateur qu'on réessaie
                    status_container.info(f"Tentative {retry_count+1}/{MAX_RETRIES}... Notre assistant fiscal est en train de se réveiller 🧠")
                
                # Appel à l'API avec un timeout plus long lors des retries
                timeout = 30 + (retry_count * 20)  # 30s, 50s, 70s...
                res = call_private_api(question, API_URL, timeout)
                res.raise_for_status()
                data = res.json()
                
                # Si on arrive ici, c'est que l'appel a réussi
                success = True
                status_container.empty()
                
                answer = data["answer"]
                reasoning = data.get("reasoning", "")
                sources = data.get("sources", [])

                # Format réponse + sources
                full_answer = answer
                
                # Traitement des sources selon leur format
                if sources:
                    source_list = []
                    for src in sources:
                        if isinstance(src, dict):
                            # Format enrichi avec métadonnées
                            meta = src.get("metadata", {})
                            if "source" in meta:
                                # Traitement spécial pour le CGI avec plus de détails
                                if "Code Général des Impôts" in meta["source"]:
                                    # Construire une description plus informative
                                    article = meta.get("article", "")
                                    theme = meta.get("theme", "")
                                    extrait = meta.get("extrait", "")
                                    
                                    if article:
                                        source_desc = f"CGI - Article {article}"
                                        if theme:
                                            source_desc += f" ({theme})"
                                    elif theme:
                                        source_desc = f"CGI - Section {theme}"
                                    elif extrait:
                                        source_desc = f"CGI - {extrait}"
                                    else:
                                        source_desc = "Code Général des Impôts"
                                    
                                    source_list.append(source_desc)
                                else:
                                    # Format standard pour les autres sources
                                    title = meta.get("title", meta.get("title_head", ""))
                                    date = meta.get("date", "")
                                    if title and date:
                                        source_list.append(f"{title} ({date})")
                                    else:
                                        source_list.append(meta["source"])
                            else:
                                source_list.append(f"Source {src.get('index', '')}")
                        else:
                            # Format simple (chaîne de caractères)
                            source_list.append(str(src))
                            
                    if source_list:
                        # Affichage des sources avec des couleurs
                        full_answer += "\n\n📚 **Sources** :\n"
                        for idx, src in enumerate(source_list):
                            # Associer des couleurs différentes selon le type de source
                            if src.startswith("CGI"):
                                color = "#3366CC"
                            elif "BOFIP" in src or "TVA" in src:
                                color = "#339933"
                            elif "Barème" in src or "BAREME" in src:
                                color = "#993399"
                            else:
                                color = "#999999"
                                
                            full_answer += f"- <span style='color:{color};'>{src}</span>\n"
                
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                # Erreurs de timeout ou de connexion (probablement un démarrage à froid)
                retry_count += 1
                error_message = "Nous préparons notre assistant fiscal pour vous répondre"
                
                if retry_count < MAX_RETRIES:
                    # Attendre avant de réessayer
                    wait_message = f"Un instant, je consulte mes ressources... ({RETRY_DELAY}s)"
                    status_container.info(wait_message)
                    time.sleep(RETRY_DELAY)
                    
            except Exception as e:
                # Autres erreurs
                retry_count += 1
                error_message = "Notre assistant fiscal rencontre des difficultés"
                
                if retry_count < MAX_RETRIES:
                    wait_message = f"Un instant, je consulte mes ressources... ({RETRY_DELAY}s)"
                    status_container.info(wait_message)
                    time.sleep(RETRY_DELAY)
        
        # Effacer le conteneur de statut
        status_container.empty()
                
        # Si toutes les tentatives ont échoué
        if not success:
            friendly_messages = [
                "🧩 Notre assistant fiscal est actuellement en train de s'initialiser.",
                "🧠 Il reviendra bientôt, prêt à répondre à toutes vos questions fiscales.",
                "⏳ Merci de réessayer dans quelques instants."
            ]
            full_answer = "\n\n".join(friendly_messages)
            reasoning = ""

    # Affiche la réponse principale dans le chat
    st.chat_message("assistant").markdown(full_answer, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": full_answer})

    # Affiche le raisonnement dans un bloc dépliant
    if reasoning:
        with st.expander("🧠 Raisonnement détaillé", expanded=False):
            st.markdown(reasoning, unsafe_allow_html=True)