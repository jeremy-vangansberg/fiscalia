from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class FlatFileData(SQLModel, table=True):
    """Modèle pour stocker les données brutes des fichiers plats"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str = Field(max_length=255)
    content: str
    processed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_type: Optional[str] = Field(max_length=50, default=None)
    status: str = Field(max_length=20, default="raw")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "filename": "bofip_stock_20240129.tgz",
                "content": "contenu du fichier...",
                "source_type": "bofip_api",
                "status": "raw"
            }
        }
    ) 