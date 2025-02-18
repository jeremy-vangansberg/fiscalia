# Gestion des Données - Data Management

## Description
Ce projet implémente un système de gestion de données répondant au référentiel de compétences E1. Il permet l'extraction, la transformation et le stockage de données depuis différentes sources vers une base de données structurée.


```mermaid
flowchart TD
    A("Bofip") --> B["Extraction du flat file\n(via requête API)"]
    C("Source Web") --> D["Extraction du flat file\n(via scraping)"]
    B --> E["Stockage des flat files"]
    D --> E
    E --> F{"Choix d'environnement"}
    F -- Local --> G["Traitement local"]
    F -- Azure --> H["Azure Data Lake Gen2"]
    G --> I["Agrégation et normalisation\n(ELT)"]
    H --> I
    I --> J[(Stockage dans une BDD)]
    J --> M["API CRUD (FastAPI)"]
```

## Compétences Couvertes

### 1. Extraction de Données (C1)
- Extraction depuis des fichiers plats (CSV, Excel)
- Scraping web avec Scrapy
- Collecte via API REST
- Gestion des erreurs et logging
- Documentation des procédures d'extraction

### 2. Requêtes SQL (C2)
- Requêtes optimisées avec indexation
- Documentation des requêtes
- Support MySQL (production) et SQLite (tests)
- Optimisation des performances

### 3. Agrégation des Données (C3)
- Nettoyage des données corrompues
- Validation des schémas
- Transformation des formats
- Documentation des règles d'agrégation

### 4. Base de Données (C4)
- Modélisation avec SQLModel
- Gestion RGPD
- Migration des données
- Documentation technique complète

### 5. API REST (C5)
- Interface FastAPI
- Documentation OpenAPI
- Gestion des erreurs
- Sécurisation des endpoints

## Structure du Projet
```
data_management/
├── src/
│   ├── data_extraction/      # C1: Extraction des données
│   │   ├── api_extractor.py
│   │   └── web_scraper.py
│   ├── models/              # C4: Modèles SQLModel
│   │   ├── __init__.py
│   │   └── data_models.py
│   ├── database/           # C2: Requêtes SQL
│   │   ├── db_manager.py
│   │   └── queries.py
│   ├── data/              # C3: Agrégation
│   │   └── data_loader.py
│   └── config/
│       └── settings.py
├── tests/                  
│   ├── conftest.py        # Fixtures pytest
│   ├── test_models/       # Tests des modèles
│   ├── test_extraction/   # Tests d'extraction
│   └── test_api/         # Tests API
└── docs/                  
    ├── database_schema.md
    └── gdpr_compliance.md
```

## Modélisation des Données (SQLModel)

### Modèles
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class FlatFileData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    content: str
    processed_at: datetime = Field(default_factory=datetime.utcnow)
    source_type: str
    status: str = Field(default="raw")
```

## Tests (pytest)

### Structure des Tests
Les tests sont organisés selon les compétences du référentiel :
```
tests/
├── conftest.py                     # Fixtures partagées
├── test_extraction/                # Tests C1
│   ├── test_api.py                
│   └── test_files.py              
├── test_sql/                      # Tests C2
│   └── test_queries.py
├── test_aggregation/              # Tests C3
│   └── test_data_cleaner.py
├── test_models/                   # Tests C4
│   └── test_data_models.py
└── test_api/                      # Tests C5
    └── test_endpoints.py
```

### Configuration des Tests
```env
# .env.test
DATABASE_URL=sqlite:///./test.db
TEST_DATABASE_URL=sqlite:///./test.db
LOG_LEVEL=DEBUG
```

### Exécution des Tests
```bash
# Tests par compétence
pytest tests/test_extraction/  # C1
pytest tests/test_sql/        # C2
pytest tests/test_aggregation/# C3
pytest tests/test_models/     # C4
pytest tests/test_api/        # C5

# Couverture de code
pytest --cov=src tests/
```

## Installation et Configuration

### Dépendances
```txt
fastapi>=0.68.0
sqlmodel>=0.0.8
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-asyncio>=0.21.0
requests>=2.28.0
scrapy>=2.5.0
```

### Variables d'Environnement
```env
DATABASE_URL=mysql://user:password@localhost/dbname
TEST_DATABASE_URL=sqlite:///./test.db
LOG_LEVEL=INFO
```

## Conformité RGPD
- Identification des données personnelles
- Procédures de nettoyage automatique
- Documentation des traitements
- Registre des opérations

## Développement

### Bonnes Pratiques
- Tests unitaires pour chaque compétence
- Documentation des fonctions et classes
- Gestion des erreurs et logging
- Couverture de code > 80%

## Contribution
1. Fork le projet
2. Créer une branche par fonctionnalité
3. Ajouter les tests correspondants
4. Vérifier la couverture de code
5. Créer une Pull Request

## Licence
Ce projet est sous licence MIT.