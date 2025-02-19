# Fiscalia Data Collection

Projet de collecte et d'analyse des données fiscales françaises. Ce projet fait partie d'une certification et vise à automatiser la collecte des données du BOFiP (Bulletin Officiel des Finances Publiques).

## Pipeline de données

```mermaid
flowchart TD
    A("Bofip") --> n1["pdf"] & n2["API"]
    B["html:data<br>xml:metadata"] --> E["Stockage des flat files"]
    E --> F@{ label: "Choix d'environnement" }
    F -- Local --> G["local"]
    F -- Azure --> H["Azure Data Lake Gen2"]
    G --> I["Ingestion en base de données"]
    H --> I
    I --> J["MySQL (+JSON)"]
    J --> M["API CRUD (FastAPI)"]
    n1 --> E
    n2 --> B

    F@{ shape: diamond}
    G@{ shape: disk}
    H@{ shape: disk}
    J@{ shape: db}
    M@{ shape: rect}
```

## Architecture

```
fiscalia_data_collection/
├── scripts/                      # Scripts d'exécution
│   ├── run_api.py               # Lance l'API
│   └── run_bofip_data_collection.py  # Pipeline de collecte BOFiP
├── src/                         # Code source
│   ├── api/                    # API FastAPI
│   ├── config/                 # Configuration
│   ├── data_extraction/        # Extracteurs de données
│   ├── data_transformation/    # Transformation des données
│   │   ├── decompressor.py    # Décompression des fichiers
│   │   └── normalizer.py      # Normalisation des données
│   ├── storage/               # Gestion du stockage
│   └── utils/                 # Utilitaires
├── docs/                      # Documentation
│   └── mermaid.MD            # Diagrammes du projet
├── notebooks/                 # Notebooks d'exploration
└── tests/                    # Tests unitaires
```

## Utilisation

Le script principal permet d'exécuter tout ou partie du pipeline de collecte :

```bash
# Pipeline complet
poetry run python scripts/run_bofip_data_collection.py

# Étapes spécifiques
poetry run python scripts/run_bofip_data_collection.py --steps extract decompress
poetry run python scripts/run_bofip_data_collection.py --steps transform

# API
poetry run python scripts/run_api.py
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