from bs4 import BeautifulSoup
from lxml import etree
from pathlib import Path
from langchain_core.documents import Document
from typing import List, Dict
import json
import logging
from tqdm import tqdm

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_document_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    return title_tag.get_text(strip=True) if title_tag else ""

def extract_metadata(xml_path: Path) -> Dict:
    tree = etree.parse(str(xml_path))
    ns = {'dc': 'http://purl.org/dc/elements/1.1'}
    relations = tree.findall('.//dc:relation', namespaces=ns)
    referenced_ids = [rel.text for rel in relations if rel.get("type") == "references"]

    return {
        "title_xml": tree.findtext('.//dc:title', namespaces=ns),
        "date": tree.findtext('.//dc:date', namespaces=ns),
        "source": tree.findtext('.//dc:source', namespaces=ns),
        "url": tree.findall('.//dc:identifier', namespaces=ns)[-1].text,
        "file": xml_path.stem,
        "references": referenced_ids
    }

def extract_sections(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol'])

    sections = []
    current = {
        "title": "Préambule",
        "level": 0,
        "content": ""
    }

    for tag in tags:
        if tag.name in ["h1", "h2", "h3"]:
            if current["content"].strip():
                sections.append(current)
            current = {
                "title": tag.get_text(strip=True),
                "level": int(tag.name[1]),
                "content": ""
            }
        else:
            current["content"] += "\n" + tag.get_text(separator=" ", strip=True)

    if current["content"].strip():
        sections.append(current)

    return sections

def html_to_documents(html_text: str, xml_path: Path) -> List[Document]:
    metadata_common = extract_metadata(xml_path)
    metadata_common["title_head"] = extract_document_title(html_text)

    sections = extract_sections(html_text)

    return [
        Document(
            page_content=section["content"],
            metadata={
                **metadata_common,
                "section": section["title"],
                "level": section["level"]
            }
        )
        for section in sections if section["content"].strip()
    ]

def process_bofip_directory(base_path: str, output_file: str):
    """
    Traite récursivement tous les documents BOFiP dans l'arborescence donnée.
    
    Args:
        base_path: Chemin vers le répertoire racine contenant les documents BOFiP
        output_file: Chemin du fichier JSONL de sortie
    """
    base_dir = Path(base_path)
    all_documents = []
    
    # Recherche tous les répertoires contenant data.html et document.xml
    html_files = list(base_dir.rglob("data.html"))
    
    for html_path in tqdm(html_files, desc="Traitement des documents"):
        try:
            xml_path = html_path.parent / "document.xml"
            if not xml_path.exists():
                logger.warning(f"Fichier XML manquant pour {html_path}")
                continue
                
            html_raw = html_path.read_text(encoding="utf-8")
            docs = html_to_documents(html_raw, xml_path)
            all_documents.extend(docs)
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement de {html_path}: {str(e)}")
            
    # Export en JSONL
    logger.info(f"Export de {len(all_documents)} documents vers {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        for doc in all_documents:
            json.dump({
                "page_content": doc.page_content,
                "metadata": doc.metadata
            }, f, ensure_ascii=False)
            f.write("\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Parser BOFiP")
    parser.add_argument("--input-dir", required=True, help="Répertoire racine contenant les documents BOFiP")
    parser.add_argument("--output-file", required=True, help="Chemin du fichier JSONL de sortie")
    
    args = parser.parse_args()
    
    process_bofip_directory(args.input_dir, args.output_file) 