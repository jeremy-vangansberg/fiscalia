# Guide d'Installation MySQL

Ce document détaille la procédure d'installation et de configuration de MySQL pour le projet Fiscalia Data Collection.

## Installation sur macOS

### 1. Installation via Homebrew
```bash
# Installation de MySQL
brew install mysql
```

### 2. Démarrage du service
```bash
# Démarrer MySQL
brew services start mysql

# Vérifier que MySQL est en cours d'exécution
brew services list | grep mysql
```

### 3. Configuration initiale
```bash
# Exécuter le script de sécurisation
mysql_secure_installation
```
Suivez les étapes :
1. Appuyez sur 'y' pour configurer le composant VALIDATE PASSWORD
2. Choisissez le niveau 0 (LOW) pour le développement
3. Définissez un mot de passe root
4. Répondez 'y' à toutes les questions suivantes :
   - Supprimer les utilisateurs anonymes
   - Désactiver la connexion root à distance
   - Supprimer la base de test
   - Recharger les privilèges

### 4. Création de l'utilisateur pour l'application
```bash
# Connexion à MySQL en tant que root
mysql -u root -p

# Dans MySQL, créez l'utilisateur et accordez les privilèges
CREATE USER 'bofip_user'@'localhost' IDENTIFIED BY 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON *.* TO 'bofip_user'@'localhost';
FLUSH PRIVILEGES;
quit;
```

### 5. Vérification
```bash
# Tester la connexion avec le nouvel utilisateur
mysql -u bofip_user -p
```

## Installation sur Ubuntu

### 1. Mise à jour du système
```bash
sudo apt update
sudo apt upgrade
```

### 2. Installation de MySQL
```bash
# Installation du serveur MySQL
sudo apt install mysql-server

# Démarrage automatique du service
sudo systemctl enable mysql

# Démarrage du service
sudo systemctl start mysql

# Vérification du statut
sudo systemctl status mysql
```

### 3. Configuration de la sécurité
```bash
# Exécuter le script de sécurisation
sudo mysql_secure_installation
```
Suivez les mêmes étapes que pour macOS.

### 4. Configuration de l'authentification
```bash
# Connexion à MySQL en tant que root
sudo mysql

# Dans MySQL, modifiez l'authentification root et créez l'utilisateur applicatif
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'votre_mot_de_passe_root';
CREATE USER 'bofip_user'@'localhost' IDENTIFIED BY 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON *.* TO 'bofip_user'@'localhost';
FLUSH PRIVILEGES;
quit;
```

### 5. Vérification
```bash
# Tester la connexion
mysql -u bofip_user -p
```

## Configuration du Projet

Une fois MySQL installé et configuré :

1. Copiez le fichier de configuration :
```bash
cp .env.example .env
```

2. Modifiez le fichier `.env` avec vos paramètres :
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=bofip
DB_USER=bofip_user
DB_PASSWORD=votre_mot_de_passe
```

3. Initialisez la base de données :
```bash
poetry run python scripts/init_database.py
```

## Résolution des problèmes courants

### Erreur "Access denied for user 'root'@'localhost'"
```bash
# Sur macOS
brew services stop mysql
mysql.server start --skip-grant-tables --skip-networking

# Dans un autre terminal
mysql
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'nouveau_mot_de_passe';
FLUSH PRIVILEGES;
quit;

# Arrêter MySQL et redémarrer normalement
mysql.server stop
brew services start mysql
```

### Erreur "Can't connect to local MySQL server through socket"
```bash
# Vérifier que MySQL est en cours d'exécution
# Sur macOS
brew services list | grep mysql

# Sur Ubuntu
sudo systemctl status mysql

# Redémarrer le service si nécessaire
# Sur macOS
brew services restart mysql

# Sur Ubuntu
sudo systemctl restart mysql
```

### Erreur de port déjà utilisé
```bash
# Vérifier quel processus utilise le port
sudo lsof -i :3306

# Si nécessaire, modifier le port dans my.cnf
# Sur macOS
echo "port=3307" | sudo tee -a /opt/homebrew/etc/my.cnf

# Sur Ubuntu
echo "port=3307" | sudo tee -a /etc/mysql/mysql.conf.d/mysqld.cnf

# Redémarrer MySQL après modification
``` 