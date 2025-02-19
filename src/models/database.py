from datetime import date, datetime
from typing import Optional
from sqlmodel import Field, SQLModel, JSON
from pydantic import condecimal


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
        index=True,
        max_length=100,
        description="Identifiant unique du document (ex: BOI-LETTRE-000048-20130826)"
    )
    title: Optional[str] = Field(default=None, max_length=255)
    publication_date: Optional[date] = Field(default=None, index=True)
    
    # Métadonnées Dublin Core
    creator: Optional[str] = Field(default=None, max_length=100)
    publisher: Optional[str] = Field(default=None, max_length=100)
    language: Optional[str] = Field(default=None, max_length=50)
    format: Optional[str] = Field(default=None, max_length=50)
    source: Optional[str] = Field(default=None, max_length=255)
    rights: Optional[str] = Field(default=None, max_length=255)
    coverage: Optional[str] = Field(default=None, max_length=255)
    subject: Optional[str] = Field(default=None, max_length=255)
    relation: Optional[str] = Field(default=None, max_length=255)
    
    # Métadonnées spécifiques BOFiP
    contenu_type: Optional[str] = Field(default=None, max_length=50)
    contenu_niveau: Optional[str] = Field(default=None, max_length=50)
    directeur_publication: Optional[str] = Field(default=None, max_length=255)
    isbn: Optional[str] = Field(default=None, max_length=50)
    
    # Informations sur les fichiers
    file_path: str = Field(max_length=500)
    data_html_file: str = Field(max_length=255)
    document_xml_file: str = Field(max_length=255)
    
    # Contenu et métadonnées
    html_content: Optional[str] = Field(default=None)
    metadata: Optional[dict] = Field(default=None, sa_column=JSON)
    
    # Métadonnées techniques
    date_import: datetime = Field(
        default_factory=datetime.now(datetime.UTC),
        nullable=False
    ) 