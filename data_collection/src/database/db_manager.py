from typing import List, Optional
from sqlmodel import SQLModel, Session, create_engine, select
from .models import FlatFileData
import logging

class DatabaseManager:
    def __init__(self, database_url: str):
        """Initialise le gestionnaire de base de données
        
        Args:
            database_url: URL de connexion à la base de données
        """
        self.database_url = database_url
        self.engine = create_engine(database_url)
        SQLModel.metadata.create_all(self.engine)
        self.logger = logging.getLogger(__name__)

    def store_flat_file_data(self, filename: str, content: str, source_type: str) -> FlatFileData:
        """Stocke les données d'un fichier plat dans la base
        
        Args:
            filename: Nom du fichier
            content: Contenu du fichier
            source_type: Type de source (ex: bofip_api, web_scraping)
            
        Returns:
            FlatFileData: L'enregistrement créé
        """
        data = FlatFileData(
            filename=filename,
            content=content,
            source_type=source_type
        )
        
        with Session(self.engine) as session:
            session.add(data)
            session.commit()
            session.refresh(data)
            return data
    
    def get_flat_file_data(self, status: Optional[str] = None) -> List[FlatFileData]:
        """Récupère les données des fichiers plats
        
        Args:
            status: Filtre optionnel sur le statut
            
        Returns:
            List[FlatFileData]: Liste des enregistrements
        """
        with Session(self.engine) as session:
            statement = select(FlatFileData)
            if status:
                statement = statement.where(FlatFileData.status == status)
            return session.exec(statement).all()
    
    def update_flat_file_status(self, file_id: int, new_status: str) -> Optional[FlatFileData]:
        """Met à jour le statut d'un fichier
        
        Args:
            file_id: ID du fichier
            new_status: Nouveau statut
            
        Returns:
            Optional[FlatFileData]: L'enregistrement mis à jour ou None si non trouvé
        """
        with Session(self.engine) as session:
            statement = select(FlatFileData).where(FlatFileData.id == file_id)
            data = session.exec(statement).first()
            if data:
                data.status = new_status
                session.add(data)
                session.commit()
                session.refresh(data)
            return data 