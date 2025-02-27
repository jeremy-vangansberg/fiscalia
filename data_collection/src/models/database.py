from datetime import date, datetime
from typing import Optional, Dict, Any
from sqlmodel import Field, SQLModel
from sqlalchemy import JSON, Text, String, DateTime, Date, Index, Column
from pydantic import validator
import datetime as dt
import re

def get_utc_now() -> datetime:
    """Retourne la date et l'heure actuelles en UTC."""
    return datetime.now(dt.UTC)

class BofipDocument(SQLModel, table=True):
    """
    Modèle SQLModel pour la table des documents BOFiP.
    
    Équivalent SQL:
    CREATE TABLE bofip_document (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_identifier VARCHAR(100) NOT NULL,
        title VARCHAR(255),
        publication_date DATE,
        creator VARCHAR(100),
        publisher VARCHAR(100),
        language VARCHAR(50),
        format VARCHAR(50),
        source VARCHAR(255),
        rights VARCHAR(255),
        coverage VARCHAR(255),
        subject VARCHAR(255),
        relation VARCHAR(255),
        contenu_type VARCHAR(50),
        contenu_niveau VARCHAR(50),
        directeur_publication VARCHAR(255),
        isbn VARCHAR(50),
        file_path VARCHAR(500),
        data_html_file VARCHAR(255),
        document_xml_file VARCHAR(255),
        html_content TEXT,
        metadata JSON,
        date_import TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX idx_document_identifier ON bofip_document(document_identifier);
    CREATE INDEX idx_publication_date ON bofip_document(publication_date);
    CREATE FULLTEXT INDEX idx_html_content ON bofip_document(html_content);
    """
    
    # Identifiants et métadonnées primaires
    id: Optional[int] = Field(default=None, primary_key=True)
    document_identifier: str = Field(
        sa_column=Column(String(100), index=True),
        description="Identifiant unique du document (ex: BOI-LETTRE-000048-20130826)"
    )
    title: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    publication_date: Optional[date] = Field(
        default=None,
        sa_column=Column(Date, index=True)
    )
    
    # Métadonnées Dublin Core
    creator: Optional[str] = Field(default=None, sa_column=Column(String(100)))
    publisher: Optional[str] = Field(default=None, sa_column=Column(String(100)))
    language: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    format: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    source: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    rights: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    coverage: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    subject: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    relation: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    
    # Métadonnées spécifiques BOFiP
    contenu_type: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    contenu_niveau: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    directeur_publication: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    isbn: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    
    # Informations sur les fichiers
    file_path: str = Field(sa_column=Column(String(500)))
    data_html_file: str = Field(sa_column=Column(String(255)))
    document_xml_file: str = Field(sa_column=Column(String(255)))
    
    # Contenu et métadonnées
    html_content: Optional[str] = Field(
        default=None,
        sa_column=Column(Text)
    )
    document_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON)
    )
    
    # Métadonnées techniques
    date_import: datetime = Field(
        default_factory=get_utc_now,
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    # Configuration des index
    __table_args__ = (
        Index('idx_document_identifier', 'document_identifier'),
        Index('idx_publication_date', 'publication_date'),
        Index('idx_html_content', 'html_content', mysql_prefix='FULLTEXT'),
    )
    
    @validator('document_identifier')
    def validate_document_identifier(cls, v: str) -> str:
        """Valide le format de l'identifiant du document.
        
        Format attendu : BOI-CATEGORIE-NUMERO-AAAAMMJJ
        Exemple : BOI-LETTRE-000048-20130826
        """
        pattern = r'^BOI-[A-Z]+-\d{6}-\d{8}$'
        if not re.match(pattern, v):
            raise ValueError(
                'document_identifier doit suivre le format BOI-CATEGORIE-NUMERO-AAAAMMJJ'
                ' (ex: BOI-LETTRE-000048-20130826)'
            )
        return v 