# Fiscalia Data Collection

Projet de collecte et d'analyse des données fiscales françaises. Ce projet fait partie d'une certification et vise à automatiser la collecte des données du BOFiP (Bulletin Officiel des Finances Publiques).

## Architecture

```
fiscalia_data_collection/
├── scripts/               # Scripts d'exécution
│   ├── run_api.py        # Lance l'API
│   ├── run_api_extraction.py  # Extraction via API
│   └── run_scraping.py   # Web scraping
├── src/                  # Code source
│   ├── api/             # API FastAPI
│   ├── config/          # Configuration
│   ├── data_extraction/ # Extracteurs de données
│   ├── data_aggregation/# Agrégation des données
│   ├── storage/         # Gestion du stockage
│   └── utils/           # Utilitaires
├── notebooks/           # Notebooks d'exploration
└── tests/              # Tests unitaires
```

## Fonctionnalités

- Extraction automatisée des données du BOFiP
- Support du stockage local et Azure Data Lake Gen2
- API REST pour accéder aux données
- Pipeline de traitement des données

## Installation

```bash
# Installation avec Poetry
poetry install
```

## Configuration

Créez un fichier `.env` basé sur `.env.example` :

```env
# Stockage (local ou azure)
STORAGE_TYPE=local

# API BOFiP
BOFIP_API_URL=https://...
BOFIP_API_LIMIT=20
```

## Utilisation

```bash
# Extraction des données
poetry run python scripts/run_api_extraction.py

# Lancement de l'API
poetry run python scripts/run_api.py
```

## Azure Data Lake Storage

Pour utiliser Azure Data Lake Gen2, configurez dans `.env` :

```env
STORAGE_TYPE=azure
AZURE_STORAGE_ACCOUNT=compte
AZURE_STORAGE_KEY=clé
AZURE_CONTAINER=container
AZURE_DIRECTORY=bofip
```

## Développement

```bash
# Tests
poetry run pytest

# Formatage
poetry run black .
poetry run isort .
```

## Licence

Apache License 2.0