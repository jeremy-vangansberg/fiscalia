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
