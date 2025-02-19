# TODO List du Projet

## 🗺️ Roadmap
1. **Phase actuelle - C1 : Extraction des données (En cours)**
   - Finalisation de l'extraction des données BOFiP
   - Documentation complète du processus

2. **Prochaine phase - C4 & C3 : Modélisation et Ingestion**
   - Conception du modèle de données
   - Mise en place de la base de données
   - Développement du script d'ingestion
   - Documentation RGPD

3. **Phase finale - C5 & C2 : API et Requêtes**
   - Développement de l'API REST
   - Conception des requêtes SQL optimisées
   - Documentation API

## 🎯 Vue d'ensemble du projet

### 📋 État d'avancement global
- [~] C1 - Automatiser l'extraction de données (70%)
- [ ] C2 - Développer des requêtes SQL d'extraction
- [ ] C3 - Développer des règles d'agrégation de données
- [ ] C4 - Créer une base de données conforme au RGPD
- [ ] C5 - Développer une API REST

## 📝 Tâches détaillées par compétence

### C1 - Automatiser l'extraction de données
#### Documentation
- [x] Rédiger la présentation du projet
  - [x] Acteurs (BOFiP, Utilisateurs)
  - [x] Objectifs fonctionnels et techniques (Extraction et mise à disposition des données fiscales)
  - [x] Environnements et contraintes techniques (Python, API BOFiP)
  - [ ] Budget
  - [x] Organisation du travail (Git, Tests)
  - [ ] Planification

#### Spécifications techniques
- [x] Documenter les technologies et outils (Python, Poetry)
- [x] Documenter les services externes (API BOFiP)
- [x] Documenter les exigences de programmation (Python 3.8+)
- [x] Documenter l'accessibilité (Configuration des chemins)

#### Développement
- [~] Implémenter le script d'extraction
  - [x] Point de lancement (scripts/run_bofip_data_collection.py)
  - [x] Initialisation des dépendances (pyproject.toml)
  - [x] Connexions externes (API BOFiP)
  - [x] Règles logiques de traitement
  - [x] Gestion des erreurs et exceptions
  - [~] Sauvegarde des résultats (En cours d'optimisation)
- [x] Versionner le code sur Git

### C2 - Développer des requêtes SQL d'extraction
*(À développer lors de la phase API)*
- [ ] Développer les requêtes SQL
- [ ] Documenter les choix de requêtes
  - [ ] Sélections
  - [ ] Filtrages
  - [ ] Conditions
  - [ ] Jointures
- [ ] Documenter les optimisations

### C3 - Développer des règles d'agrégation de données
#### Script d'agrégation
- [ ] Développer le script d'ingestion
  - [ ] Validation des données
  - [ ] Transformation au format base de données
  - [ ] Gestion des mises à jour
- [ ] Versionner le code

#### Documentation
- [ ] Documenter les dépendances
- [ ] Documenter les commandes
- [ ] Documenter l'algorithme d'ingestion
- [ ] Documenter les transformations
- [ ] Documenter la stratégie de mise à jour

### C4 - Créer une base de données conforme au RGPD
#### Modélisation (Prioritaire)
- [ ] Créer le modèle conceptuel (MCD)
  - [ ] Identifier les entités principales
  - [ ] Définir les relations
  - [ ] Documenter les cardinalités
- [ ] Créer le modèle physique (MPD)
- [ ] Choisir le SGBD adapté (PostgreSQL envisagé)

#### Implémentation
- [ ] Créer la base de données
- [ ] Développer le script d'import
- [ ] Documenter l'installation
- [ ] Documenter les dépendances
- [ ] Documenter les commandes

#### RGPD
- [ ] Créer le registre des traitements
- [ ] Rédiger les procédures de tri
- [ ] Documenter la fréquence d'exécution

### C5 - Développer une API REST
*(À développer après la base de données)*
#### Documentation
- [ ] Documenter les endpoints
- [ ] Documenter l'authentification
- [ ] Documenter les autorisations
- [ ] Utiliser le standard OpenAPI

#### Développement
- [ ] Implémenter l'authentification
- [ ] Implémenter les endpoints
- [ ] Tester l'API

## 📊 Suivi des progrès

### Points forts actuels
- Architecture modulaire bien structurée
- Tests unitaires en place
- Gestion des configurations robuste
- Extraction des données BOFiP fonctionnelle

### Points à améliorer
- Documentation du projet à compléter
- Planification détaillée à établir
- Réflexion sur la modélisation des données à approfondir

### Prochaines étapes prioritaires
1. Finaliser la documentation C1
2. Commencer la modélisation de la base de données (C4)
3. Concevoir le script d'ingestion (C3)

## 💡 Notes et idées
- Utiliser PostgreSQL avec JSONB pour la flexibilité du schéma
- Prévoir une stratégie de mise à jour incrémentale des données
- Considérer l'utilisation de FastAPI pour l'API REST

---
*Dernière mise à jour : 19 février 2024* 