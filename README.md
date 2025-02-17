# Gestion des Données - Data Management

## Description
Ce projet implémente un système de gestion de données répondant au référentiel de compétences E1. Il permet l'extraction, la transformation et le stockage de données depuis différentes sources vers une base de données structurée.

## Structure du Projet
```
data_management/
├── src/
│   ├── data_extraction/      # Extraction des données (C1)
│   │   ├── api_extractor.py
│   │   └── web_scraper.py
│   ├── models/              # Modèles SQLModel (C4)
│   │   ├── __init__.py
│   │   └── data_models.py
│   ├── database/           
│   │   ├── db_manager.py
│   │   └── queries.py
│   ├── data/               
│   │   └── data_loader.py
│   └── config/
│       └── settings.py
├── tests/                  
│   ├── conftest.py        # Fixtures pytest
│   ├── test_models/       # Tests des modèles
│   ├── test_extraction/   # Tests d'extraction
│   └── test_api/         # Tests API
└── docs/                  
    └── database_schema.md
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
```
tests/
├── conftest.py                # Fixtures partagées
├── test_models/
│   └── test_data_models.py    # Tests des modèles SQLModel
├── test_extraction/
│   ├── test_api.py            # Tests d'extraction API
│   └── test_files.py          # Tests des fichiers plats
└── test_api/
    └── test_endpoints.py      # Tests des endpoints FastAPI
```

### Fixtures pytest
```python
@pytest.fixture(scope="session")
def test_db():
    """Fixture de base de données SQLite pour les tests"""
    database_url = "sqlite:///./test.db"
    engine = create_engine(database_url)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
```

### Exécution des Tests
```bash
# Exécuter tous les tests avec couverture
pytest --cov=src tests/

# Exécuter des tests spécifiques
pytest tests/test_models/
pytest tests/test_extraction/

# Tests avec rapport détaillé
pytest --verbose --cov=src --cov-report=html tests/
```

## Installation

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Dépendances Principales
```txt
fastapi>=0.68.0
sqlmodel>=0.0.8
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-asyncio>=0.21.0
requests>=2.28.0
scrapy>=2.5.0
```

## Configuration
1. Copier `.env.example` vers `.env`
2. Configurer les variables d'environnement :
```env
DATABASE_URL=mysql://user:password@localhost/dbname
TEST_DATABASE_URL=sqlite:///./test.db
LOG_LEVEL=INFO
```

## Développement

### Bonnes Pratiques de Test
- Utiliser des fixtures pytest pour la réutilisation du code
- Tester avec une base SQLite en mémoire pour la rapidité
- Implémenter des tests d'intégration avec la base MySQL
- Utiliser pytest.mark pour organiser les tests
- Maintenir une couverture de code > 80%

### Exemple de Test
```python
def test_create_data(test_db):
    """Test la création de données avec SQLModel"""
    data = FlatFileData(
        filename="test.csv",
        content="test content",
        source_type="flat_file"
    )
    with Session(test_db) as session:
        session.add(data)
        session.commit()
        session.refresh(data)
        
    assert data.id is not None
    assert data.status == "raw"
```

## Contribution
1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Ajouter des tests pour les nouvelles fonctionnalités
4. Vérifier que tous les tests passent
5. Créer une Pull Request

## Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Contact
Pour toute question ou suggestion, merci de créer une issue dans le projet.