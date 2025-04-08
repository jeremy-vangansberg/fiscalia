from fastapi import FastAPI, Query
from pydantic import BaseModel
from app.rag_predictor import answer_question

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(payload: QueryRequest):
    result = answer_question(payload.question)
    return {
        "answer": result["answer"],
        "reasoning": result["reasoning"]
    }
