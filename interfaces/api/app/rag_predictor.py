from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document


import os

# Chargement des FAISS locaux
BASE_PATH = os.path.join(os.path.dirname(__file__), "vector_stores")
embeddings = VertexAIEmbeddings(
    model_name=os.getenv("MODEL_NAME_EMBEDDING"),
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION")
)

def load_db(name):
    return FAISS.load_local(
        os.path.join(BASE_PATH, name),
        embeddings,
        allow_dangerous_deserialization=True
    )

db_cgi = load_db("cgi")
db_bofip = load_db("bofip")
db_bofip_bareme = load_db("bofip_bareme")

llm = VertexAI(
    model_name=os.getenv("MODEL_NAME_LLM"),
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("LOCATION"),
    temperature=os.getenv("TEMPERATURE_LLM")
)

prompt_template = """
Tu es un assistant fiscal expert du Code Général des Impôts et du BOFiP. 
Tu dois répondre aux questions de manière claire, structurée et précise.
Tu vas vérifier les documents suivants pour répondre aux questions :
1. Le Code Général des Impôts (CGI)
2. Le BOFiP (Bulletin Officiel des Finances Publiques)
3. Le Barème des indemnités kilométriques.

Si la question nécessite un calcul (par exemple des montants ou des indemnités), tu utiliseras les outils de calcul disponibles.

Si aucun document spécifique n’est trouvé, tu répondras selon ta connaissance générale en fiscalité, mais tu indiqueras toujours quand tu n'as pas trouvé de réponse dans les documents fournis.

---

Contexte :
{context}

Question :
{question}

Réponse :
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

import re

def extract_final_answer(text: str) -> str:
    # Essaie de capturer la première ligne contenant un montant en euros
    match = re.search(r"(\d[\d\s]*€)", text)
    if match:
        return match.group(0)
    # Sinon, fallback à la première ligne
    return text.splitlines()[0] if text else "Aucune réponse extraite."

def answer_question(query: str) -> dict:
    embedded_query = embeddings.embed_query(query)

    docs_cgi = db_cgi.similarity_search_by_vector(embedded_query, k=3)
    docs_bofip = db_bofip.similarity_search_by_vector(embedded_query, k=3)
    docs_bareme = db_bofip_bareme.similarity_search_by_vector(embedded_query, k=3)

    def generate_answer_with_context(docs: list[Document]) -> str:
        context = "\n\n".join(doc.page_content for doc in docs)
        inputs = {"context": context, "question": query}
        return llm.invoke(prompt.format(**inputs))

    reasoning = "\n\n".join([
        generate_answer_with_context(docs_cgi),
        generate_answer_with_context(docs_bofip),
        generate_answer_with_context(docs_bareme)
    ])
    final_answer = extract_final_answer(reasoning)

    return {"answer": final_answer, "reasoning": reasoning}

