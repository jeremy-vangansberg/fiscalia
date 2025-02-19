#!/usr/bin/env python3
import sys
import mysql.connector
from pathlib import Path

# Ajouter le chemin du projet au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config.settings import settings

def test_mysql_connection():
    """
    Teste la connexion à MySQL et affiche les informations de débogage.
    """
    print("\n🔍 Test de la connexion MySQL...")
    print(f"  Host: {settings.DB_HOST}")
    print(f"  Port: {settings.DB_PORT}")
    print(f"  User: {settings.DB_USER}")
    
    try:
        # Test de connexion simple
        conn = mysql.connector.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        
        cursor = conn.cursor()
        
        # Vérifier la version de MySQL
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"✅ Connexion réussie à MySQL version: {version}")
        
        # Lister les bases de données existantes
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        print("\n📁 Bases de données existantes:")
        for db in databases:
            print(f"  - {db}")
            
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"\n❌ Erreur de connexion MySQL: {err}")
        print("\n🔍 Diagnostic:")
        if err.errno == 2003:
            print("  → MySQL n'est pas en cours d'exécution ou le port est incorrect")
            print("  → Vérifiez que MySQL est démarré:")
            print("    - Sur macOS: brew services list")
            print("    - Sur Linux: sudo systemctl status mysql")
        elif err.errno == 1045:
            print("  → Les identifiants de connexion sont incorrects")
            print("  → Vérifiez que l'utilisateur existe et a le bon mot de passe:")
            print("    mysql -u root -p")
            print("    SELECT User, Host FROM mysql.user;")
        return False

def create_database():
    """
    Crée la base de données si elle n'existe pas déjà.
    Configure également les paramètres nécessaires comme l'encodage UTF-8.
    """
    if not test_mysql_connection():
        sys.exit(1)
        
    try:
        # Connexion à MySQL sans spécifier de base de données
        conn = mysql.connector.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        
        cursor = conn.cursor()
        
        # Création de la base de données avec le bon encodage
        cursor.execute(f"""
            CREATE DATABASE IF NOT EXISTS {settings.DB_NAME}
            CHARACTER SET utf8mb4
            COLLATE utf8mb4_unicode_ci
        """)
        
        print(f"✅ Base de données '{settings.DB_NAME}' créée avec succès")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de la création de la base de données : {err}")
        print("\n💡 Assurez-vous que :")
        print("  1. MySQL est installé et en cours d'exécution")
        print("  2. Les informations de connexion dans .env sont correctes")
        print("  3. L'utilisateur a les droits suffisants pour créer une base de données")
        sys.exit(1)

def init_tables():
    """
    Initialise les tables de la base de données via SQLModel.
    """
    try:
        from src.config.database import init_db
        init_db()
        print("✅ Tables créées avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")
        sys.exit(1)

def main():
    """
    Script principal d'initialisation de la base de données.
    """
    print("🚀 Initialisation de la base de données...")
    
    # 1. Création de la base de données
    create_database()
    
    # 2. Création des tables via SQLModel
    init_tables()
    
    print("✨ Initialisation de la base de données terminée avec succès !")

if __name__ == "__main__":
    main() 