import pandas as pd
from typing import Union
import logging

class DataCleaner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def remove_corrupted_entries(self, data: pd.DataFrame, rules: dict) -> pd.DataFrame:
        """
        Supprime les entrées corrompues selon les règles définies
        """
        try:
            clean_data = data.copy()
            for column, rule in rules.items():
                if rule.get('null_check'):
                    clean_data = clean_data.dropna(subset=[column])
                if rule.get('type_check'):
                    clean_data = clean_data[clean_data[column].apply(
                        lambda x: isinstance(x, rule['type_check'])
                    )]
            return clean_data
        except Exception as e:
            self.logger.error(f"Erreur lors du nettoyage: {str(e)}")
            raise 