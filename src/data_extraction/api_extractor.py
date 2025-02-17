from typing import Dict, Any
import requests
import logging
from fastapi import HTTPException

class APIExtractor:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

    async def extract(self, endpoint: str, params: Dict[str, Any] = None) -> Dict:
        """
        Extrait les données depuis une API REST
        """
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            response = self.session.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erreur lors de l'extraction API: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e)) 