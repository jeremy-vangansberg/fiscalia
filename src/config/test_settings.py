from .settings import Settings

class TestSettings(Settings):
    # Surcharge pour utiliser SQLite en test
    DATABASE_TYPE: str = "sqlite"
    DATABASE_URL: str = "sqlite:///./test.db"
    
    class Config:
        env_file = ".env.test" 