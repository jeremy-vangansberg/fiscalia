from typing import Any, Dict, List
import pandas as pd
import logging
from pathlib import Path

class DataLoader:
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.logger = logging.getLogger(__name__)

    def load_flat_file(self, filename: str) -> pd.DataFrame:
        """
        Charge les données depuis un fichier plat
        """
        try:
            file_path = self.data_path / filename
            if file_path.suffix == '.csv':
                return pd.read_csv(file_path)
            elif file_path.suffix == '.xlsx':
                return pd.read_excel(file_path)
            else:
                raise ValueError(f"Format de fichier non supporté: {file_path.suffix}")
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement du fichier {filename}: {str(e)}")
            raise

    def validate_data(self, data: pd.DataFrame, schema: Dict[str, Any]) -> bool:
        """
        Valide les données selon un schéma défini
        """
        try:
            # Vérifie les colonnes requises
            required_columns = schema.get('required_columns', [])
            if not all(col in data.columns for col in required_columns):
                return False

            # Vérifie les types de données
            for col, dtype in schema.get('dtypes', {}).items():
                if not all(isinstance(x, dtype) for x in data[col].dropna()):
                    return False

            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de la validation des données: {str(e)}")
            return False

    def load_data(self):
        # Votre code de chargement de données
        pass 