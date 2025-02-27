from sqlmodel import create_engine, Session, SQLModel
from src.config.settings import settings

# Création de l'URL de connexion à la base de données
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Création du moteur de base de données
engine = create_engine(
    DATABASE_URL,
    echo=settings.DB_ECHO,  # Active les logs SQL en mode debug
    pool_pre_ping=True,     # Vérifie la connexion avant utilisation
)

def init_db():
    """Initialise la base de données en créant toutes les tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Crée une nouvelle session de base de données."""
    with Session(engine) as session:
        yield session 