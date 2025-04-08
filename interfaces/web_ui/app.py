import streamlit as st
import requests
import os 


API_URL = os.getenv("API_URL", "http://api:8080/ask")

st.set_page_config(page_title="Fiscalia - Assistant fiscal", page_icon="💼")

st.title("💬 Assistant fiscal - Fiscalia")
st.markdown("Pose ta question liée au Code Général des Impôts ou à la BOFiP.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affiche l'historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Formulaire utilisateur
question = st.chat_input("Ta question ici...")

if question:
    # Affiche la question
    st.chat_message("user").markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Appelle l'API
    with st.spinner("Réflexion en cours..."):
        try:
            res = requests.post(API_URL, json={"question": question}, timeout=30)
            res.raise_for_status()
            data = res.json()
            answer = data["answer"]
            reasoning = data.get("reasoning", "")
            sources = data.get("sources", [])

            # Format réponse + sources
            full_answer = answer
            if sources:
                full_answer += "\n\n📚 **Sources** :\n" + "\n".join(f"- {src}" for src in sources)

        except Exception as e:
            full_answer = f"❌ Une erreur est survenue : {e}"
            reasoning = ""

    # Affiche la réponse principale dans le chat
    st.chat_message("assistant").markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # Affiche le raisonnement dans un bloc dépliant
    with st.expander("🧠 Raisonnement détaillé"):
        st.markdown(reasoning)