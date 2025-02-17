from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import pandas as pd
import logging

class DatabaseManager:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.logger = logging.getLogger(__name__)

    def init_db(self):
        """Initialise la base de données"""
        Base.metadata.create_all(bind=self.engine)

    def store_flat_file_data(self, df: pd.DataFrame, filename: str):
        """
        Stocke les données d'un fichier plat dans la base de données
        """
        session = self.SessionLocal()
        try:
            for _, row in df.iterrows():
                flat_file_data = FlatFileData(
                    filename=filename,
                    content=row.to_json(),
                    source_type='flat_file'
                )
                session.add(flat_file_data)
            session.commit()
        except Exception as e:
            self.logger.error(f"Erreur lors du stockage des données: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close() 