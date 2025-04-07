from pathlib import Path
from bs4 import BeautifulSoup
from lxml import etree
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

def format_table_as_text(table_tag) -> str:
    """Formate une balise <table> HTML en texte lisible type Markdown."""
    rows = table_tag.find_all("tr")
    formatted_rows = []

    for row in rows:
        cols = row.find_all(["td", "th"])
        cell_texts = [col.get_text(strip=True) for col in cols]
        formatted_rows.append(" | ".join(cell_texts))

    return "\n".join(formatted_rows)

def extract_sections_with_tables(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all(['h1', 'h2', 'h3', 'p', 'ul', 'ol', 'table'])

    sections = []
    current = {
        "title": "Préambule",
        "level": 0,
        "content": "",
        "type": "text"
    }

    for tag in tags:
        if tag.name in ["h1", "h2", "h3"]:
            if current["content"].strip():
                sections.append(current)
            current = {
                "title": tag.get_text(strip=True),
                "level": int(tag.name[1]),
                "content": "",
                "type": "text"
            }
        elif tag.name == "table":
            # 🔁 Génération d’un résumé textuel du tableau
            table_rows = tag.find_all("tr")
            if not table_rows:
                continue

            headers = [cell.get_text(strip=True) for cell in table_rows[0].find_all(["th", "td"])]
            rows = [
                [cell.get_text(strip=True) for cell in tr.find_all("td")]
                for tr in table_rows[1:]
            ]

            bullet_points = []
            for row in rows:
                if len(row) != len(headers):
                    continue  # skip malformées
                intro = f"Pour {headers[0].lower()} {row[0]}"
                conditions = [
                    f"{headers[i]} → {row[i]}" for i in range(1, len(headers))
                ]
                bullet_points.append(f"{intro}, " + ", ".join(conditions))

            table_text = "\n".join(f"- {bp}" for bp in bullet_points)

            sections.append({
                "title": "Résumé du tableau",
                "level": 4,
                "content": table_text,
                "type": "table"
            })

        else:
            current["content"] += "\n" + tag.get_text(separator=" ", strip=True)

    if current["content"].strip():
        sections.append(current)

    return sections


def html_to_documents_with_tables(html_text: str, xml_path: Path) -> List[Document]:
    metadata_common = extract_metadata(xml_path)
    metadata_common["title_head"] = extract_document_title(html_text)

    sections = extract_sections_with_tables(html_text)

    return [
        Document(
            page_content=section["content"],
            metadata={
                **metadata_common,
                "section": section.get("title", "Inconnu"),
                "level": section.get("level", 0),
                "type": section.get("type", "text")
            }
        )
        for section in sections if section.get("content", "").strip()
    ]

def process_bofip_directory_with_tables(base_path: str, output_file: str):
    base_dir = Path(base_path)
    all_documents = []

    html_files = list(base_dir.rglob("data.html"))

    for html_path in tqdm(html_files, desc="Traitement des documents (avec tables)"):
        try:
            xml_path = html_path.parent / "document.xml"
            if not xml_path.exists():
                logger.warning(f"Fichier XML manquant pour {html_path}")
                continue

            html_raw = html_path.read_text(encoding="utf-8")
            docs = html_to_documents_with_tables(html_raw, xml_path)
            all_documents.extend(docs)

        except Exception as e:
            logger.error(f"Erreur lors du traitement de {html_path}: {type(e).__name__} - {str(e)}")

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
    parser = argparse.ArgumentParser(description="Parser BOFiP avec gestion des tableaux")
    parser.add_argument("--input-dir", required=True, help="Répertoire racine contenant les documents BOFiP")
    parser.add_argument("--output-file", required=True, help="Chemin du fichier JSONL de sortie")
    args = parser.parse_args()

    process_bofip_directory_with_tables(args.input_dir, args.output_file)
