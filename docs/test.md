```mermaid

erDiagram
    PRODUIT {
      int id PK
      string nom
      string description
    }
    REGLEMETEO {
      int id PK
      int produit_id FK "référence PRODUIT.id"
      string conditions "JSON"
    }
    LIEU {
      int id PK
      string nom
      float latitude
      float longitude
    }
    OBSERVATION_METEO {
      int id PK
      int lieu_id FK "référence LIEU.id"
      datetime date
      float humidity
      float wind
      float clouds
      /* Autres métriques si nécessaire */
    }

    PRODUIT ||--o{ REGLEMETEO : "produit_id"
    LIEU ||--o{ OBSERVATION_METEO : "lieu_id"


```