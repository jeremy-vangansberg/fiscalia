from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .schemas import DataResponse
from ..database.db_manager import DatabaseManager
from ..config.settings import settings

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION
)

# Injection de dépendance pour la base de données
def get_db():
    db = DatabaseManager(settings.DATABASE_URL)
    return next(db.get_session())

@app.get(f"{settings.API_PREFIX}/data", response_model=List[DataResponse])
async def get_data(db: Session = Depends(get_db)):
    try:
        # Logique de récupération des données
        return {"status": "success", "data": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 