from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import xml.etree.ElementTree as ET
import logging
from bs4 import BeautifulSoup

from src.models.database import BofipDocument
from src.data_transformation.normalizer import normalize_text, parse_date

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Traite les fichiers XML des documents BOFiP et extrait les données."""
    
    def __init__(self):
        """Initialise le processeur de documents."""
        self.required_fields = {
            'document_identifier',
            'title',
            'publication_date',
            'file_path',
            'data_html_file',
            'document_xml_file'
        }
    
    def process_document(self, xml_path: Path) -> Optional[BofipDocument]:
        """
        Traite un fichier XML et crée une instance de BofipDocument.
        
        Args:
            xml_path: Chemin du fichier XML à traiter
            
        Returns:
            Instance de BofipDocument ou None si le traitement échoue
        """
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Extraction des métadonnées
            metadata = self._extract_metadata(root)
            
            # Vérification des champs requis
            if not self._validate_required_fields(metadata):
                logger.error(f"Champs requis manquants dans {xml_path}")
                return None
            
            # Extraction du contenu HTML
            html_content = self._extract_html_content(xml_path)
            
            # Création du document
            return self._create_document(metadata, html_content, xml_path)
            
        except ET.ParseError as e:
            logger.error(f"Erreur de parsing XML pour {xml_path}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erreur lors du traitement de {xml_path}: {str(e)}")
            return None
    
    def _extract_metadata(self, root: ET.Element) -> Dict[str, Any]:
        """
        Extrait les métadonnées du document XML.
        
        Args:
            root: Élément racine du document XML
            
        Returns:
            Dictionnaire des métadonnées
        """
        metadata = {}
        
        # Mapping des champs XML vers les attributs du modèle
        field_mapping = {
            'identifier': 'document_identifier',
            'title': 'title',
            'date': 'publication_date',
            'creator': 'creator',
            'publisher': 'publisher',
            'language': 'language',
            'format': 'format',
            'source': 'source',
            'rights': 'rights',
            'coverage': 'coverage',
            'subject': 'subject',
            'relation': 'relation'
        }
        
        for xml_field, model_field in field_mapping.items():
            element = root.find(f".//{xml_field}")
            if element is not None and element.text:
                metadata[model_field] = normalize_text(element.text)
        
        # Traitement spécial pour la date
        if 'publication_date' in metadata:
            metadata['publication_date'] = parse_date(metadata['publication_date'])
        
        return metadata
    
    def _validate_required_fields(self, metadata: Dict[str, Any]) -> bool:
        """
        Vérifie la présence des champs requis.
        
        Args:
            metadata: Dictionnaire des métadonnées
            
        Returns:
            True si tous les champs requis sont présents
        """
        return all(field in metadata for field in self.required_fields)
    
    def _extract_html_content(self, xml_path: Path) -> Optional[str]:
        """
        Extrait le contenu HTML associé au document.
        
        Args:
            xml_path: Chemin du fichier XML
            
        Returns:
            Contenu HTML normalisé ou None
        """
        try:
            html_path = xml_path.parent / f"{xml_path.stem}.html"
            if not html_path.exists():
                return None
                
            with open(html_path, 'r', encoding='utf-8') as f:
                html = f.read()
                
            # Nettoyage du HTML avec BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            return str(soup)
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction du HTML pour {xml_path}: {str(e)}")
            return None
    
    def _create_document(
        self,
        metadata: Dict[str, Any],
        html_content: Optional[str],
        xml_path: Path
    ) -> BofipDocument:
        """
        Crée une instance de BofipDocument à partir des données extraites.
        
        Args:
            metadata: Métadonnées du document
            html_content: Contenu HTML
            xml_path: Chemin du fichier XML
            
        Returns:
            Instance de BofipDocument
        """
        # Ajout des chemins de fichiers
        metadata.update({
            'file_path': str(xml_path.parent),
            'data_html_file': f"{xml_path.stem}.html",
            'document_xml_file': xml_path.name,
            'html_content': html_content,
            'date_import': datetime.utcnow()
        })
        
        return BofipDocument(**metadata) 