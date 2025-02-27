from datetime import datetime, date
import re
from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)

def normalize_text(text: Optional[str]) -> Optional[str]:
    """
    Normalise un texte en supprimant les espaces superflus et les caractères spéciaux.
    
    Args:
        text: Texte à normaliser
        
    Returns:
        Texte normalisé ou None
    """
    if not text:
        return None
        
    # Suppression des espaces multiples
    text = re.sub(r'\s+', ' ', text)
    # Suppression des espaces en début et fin
    text = text.strip()
    # Remplacement des caractères spéciaux
    text = text.replace('\n', ' ').replace('\r', ' ')
    
    return text

def parse_date(date_str: str) -> Optional[date]:
    """
    Parse une date à partir d'une chaîne de caractères.
    Gère plusieurs formats de date possibles.
    
    Args:
        date_str: Date sous forme de chaîne de caractères
        
    Returns:
        Objet date ou None si le parsing échoue
    """
    date_formats = [
        '%Y-%m-%d',      # 2024-02-18
        '%d/%m/%Y',      # 18/02/2024
        '%Y%m%d',        # 20240218
        '%d-%m-%Y'       # 18-02-2024
    ]
    
    # Nettoyage de la chaîne
    date_str = normalize_text(date_str)
    if not date_str:
        return None
    
    # Essai des différents formats
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format).date()
        except ValueError:
            continue
    
    logger.warning(f"Impossible de parser la date: {date_str}")
    return None

def normalize_identifier(identifier: str) -> str:
    """
    Normalise un identifiant de document BOFiP.
    
    Args:
        identifier: Identifiant à normaliser
        
    Returns:
        Identifiant normalisé
    
    Example:
        >>> normalize_identifier("boi-lettre-000048-20130826")
        "BOI-LETTRE-000048-20130826"
    """
    if not identifier:
        raise ValueError("L'identifiant ne peut pas être vide")
    
    # Mise en majuscules et suppression des espaces
    identifier = identifier.upper().strip()
    
    # Vérification du format
    pattern = r'^BOI-[A-Z]+-\d{6}-\d{8}$'
    if not re.match(pattern, identifier):
        raise ValueError(
            f"Format d'identifiant invalide: {identifier}. "
            "Format attendu: BOI-CATEGORIE-NUMERO-AAAAMMJJ"
        )
    
    return identifier 