import streamlit as st

EXAMPLE_QUESTIONS = [
    {"title": "TVA", "description": "Comment fonctionne la TVA en France?", "category": "TVA"},
    {"title": "IR", "description": "Quel est le barème de l'impôt sur le revenu pour 2024?", "category": "Impôts"},
    {"title": "IK", "description": "Comment calculer les indemnités kilométriques pour une voiture de 6CV?", "category": "Frais"},
    {"title": "Micro", "description": "Quelles sont les charges sociales pour une micro-entreprise?", "category": "Micro"},
]

def set_question(question):
    st.session_state.question_to_ask = question

def render_sidebar(include_examples=True):
    with st.sidebar:
        st.markdown("<h1>Fiscalia</h1>", unsafe_allow_html=True)
        st.page_link("app.py", label="Assistant fiscal", icon="💬")
        st.page_link("pages/architecture.py", label=" Architecture", icon="🏗️")

        if include_examples :
            st.subheader("Exemples de questions")
            for i, example in enumerate(EXAMPLE_QUESTIONS):
                st.button(example["description"], key=f"btn_{i}", on_click=set_question, args=(example["description"],))

        st.subheader("À propos")
        st.markdown("""
            **Fiscalia** est un assistant fiscal intelligent basé sur l'IA.
            Il s'appuie sur :
            - Le Code Général des Impôts
            - Le BOFiP
            - Les barèmes fiscaux à jour
        """)

        st.subheader("Mentions légales")
        with st.expander("Mentions légales"):
            st.write("Les réponses sont données à titre informatif uniquement.")
