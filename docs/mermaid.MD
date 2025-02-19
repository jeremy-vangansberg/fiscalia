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
