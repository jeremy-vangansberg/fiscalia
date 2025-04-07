from langchain_google_vertexai import VertexAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

import os

# Chargement des FAISS locaux
BASE_PATH = "app/vector_stores"
embeddings = VertexAI(model_name="text-embedding-004")

def load_db(name):
    return FAISS.load_local(
        os.path.join(BASE_PATH, name),
        embeddings,
        allow_dangerous_deserialization=True
    )

db_cgi = load_db("cgi_faiss")
db_bofip = load_db("bofip_faiss")
db_bofip_bareme = load_db("bofip_bareme_faiss")

llm = VertexAI(model_name="gemini-2.0-flash-lite", temperature=0.3)

prompt_template = """
Tu es un assistant fiscal expert du Code Général des Impôts et du BOFiP.

Tu dois répondre à la question suivante de manière claire, structurée et précise.
Ta réponse doit **prioritairement** s’appuyer sur les extraits de documents fournis.
Tu peux utiliser tes **connaissances fiscales générales** si les extraits sont insuffisants, à condition de l’indiquer explicitement dans ta réponse.

Extrait :
Puissance administrative | Jusqu'à 5 000 km | De 5001 à 20 000 km | Au delà de 20 000 km
7 CV et plus | d x 0,697 | (d x 0,394) + 1515 | d x 0,470

Question :
Quel est le montant des indemnités kilométriques pour 7 CV et 5500 km ?

Réponse :
Pour un véhicule de 7 CV ayant parcouru 5500 km, la formule applicable est : (5500 × 0,394) + 1515 = 3 682 €.

---

Contexte :
{context}

Question :
{question}

Réponse :
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

def build_rag_chain(retriever):
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

# RAG pipelines
qa_cgi = build_rag_chain(db_cgi.as_retriever(search_kwargs={"k": 3}))
qa_bofip = build_rag_chain(db_bofip.as_retriever(search_kwargs={"k": 3}))
qa_bareme = build_rag_chain(db_bofip_bareme.as_retriever(search_kwargs={"k": 3}))

def answer_question(query: str) -> str:
    result_cgi = qa_cgi.invoke(query)
    result_bofip = qa_bofip.invoke(query)
    result_bareme = qa_bareme.invoke(query)

    parts = [result_cgi["result"], result_bofip["result"], result_bareme["result"]]
    return "\n\n".join(parts)
