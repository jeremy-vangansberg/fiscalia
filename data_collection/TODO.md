# TODO List - Critères d'Évaluation

## C1. Automatiser l'extraction de données
- [ ] La présentation du projet et de son contexte est complète : acteurs, objectifs fonctionnels et techniques, environnements et contraintes techniques, budget, organisation du travail et planification
- [ ] Les spécifications techniques précisent : les technologies et outils, les services externes, les exigences de programmation (langages), l'accessibilité (disponibilité, accès)
- [ ] Le périmètre des spécifications techniques est complet : il couvre l'ensemble des moyens techniques à mettre en œuvre pour l'extraction et l'agrégation des données en un jeu de données brutes final
- [x] Le script d'extraction des données est fonctionnel : toutes les données visées sont effectivement récupérées à l'issue de l'exécution du script
- [x] Le script comprend un point de lancement, l'initialisation des dépendances et des connexions externes, les règles logiques de traitement, la gestion des erreurs et des exceptions, la fin du traitement et la sauvegarde des résultats
- [x] Le script d'extraction des données est versionné et accessible depuis un dépôt Git
- [x] L'extraction des données est faite depuis un mix entre au moins les sources suivantes : un service web (API REST), un fichier de données, un scraping, une base de données et un système big data

## C2. Développer des requêtes SQL d'extraction
- [ ] Les requêtes de type SQL pour la collecte de données sont fonctionnelles : les données visées sont effectivement extraites suites à l'exécution des requêtes
- [ ] La documentation des requêtes met en lumière choix de sélections, filtrages, conditions, jointures, etc., en fonction des objectifs de collecte
- [ ] La documentation explicite les optimisations appliquées aux requêtes

## C3. Développer des règles d'agrégation de données
- [ ] Le script d'agrégation des données est fonctionnel : les données sont effectivement agrégées, nettoyées et normalisées en un seul jeu de données à l'issue de l'exécution du script
- [x] Le script d'agrégation des données est versionné et accessible depuis un dépôt Git
- [ ] La documentation du script d'agrégation est complète : dépendances, commandes, les enchaînements logiques de l'algorithme, les choix de nettoyage et d'homogénéisation des formats données

## C4. Créer une base de données conforme au RGPD
- [x] Les modélisations des données respectent la méthode et le formalisme Merise
- [ ] Le modèle physique des données est fonctionnel : il est intégré avec succès lors de la création de la base de données, sans erreur
- [ ] La base de données est choisie au regard de la modélisation des données et des contraintes du projet
- [ ] La reproduction des procédures d'installation décrites (base de données et API) a pour résultat un système conforme aux objets techniques attendus
- [ ] Le script d'import fourni est fonctionnel : il permet l'insertion des données dans le système mis en place
- [ ] La documentation technique du script d'import est versionné à la racine du même dépôt Git que celui utilisé pour le script d'import
- [ ] Les documentations techniques des scripts couvrent les dépendances nécessaires pour la réutilisation des scripts et les commandes pour l'exécution
- [ ] Le registre des traitements de données personnelles intègre l'ensemble des traitements de données personnelles impliqués dans la base de données
- [ ] Les procédures de tri des données personnelles pour la mise en conformité de la base de données avec le RGPD sont rédigées
- [ ] Les procédures de tri détaillent les traitements de conformité (automatisés ou non) à appliquer ainsi que leur fréquence d'exécution

## C5. Développer une API REST
- [ ] La documentation technique de l'API (REST) couvre tous les points de terminaisons
- [ ] La documentation technique couvre les règles d'authentification et/ou d'autorisation de l'API
- [ ] La documentation technique respecte les standards du modèle choisi (par exemple OpenAPI)
- [ ] L'API REST est fonctionnelle pour l'accès aux données du projet : elle restreint par une autorisation (ou authentification) l'accès aux données
- [ ] L'API REST est fonctionnelle pour la mise à disposition : elle permet la récupération de l'ensemble des données nécessaires au projet, comme prévu selon les spécifications données