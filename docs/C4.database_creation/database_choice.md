# Choix de la Base de Données : MySQL

Ce document justifie le choix de MySQL comme SGBD pour le projet, en lien avec la modélisation des données et les contraintes spécifiques de notre projet.

## Contexte du Projet

Le projet consiste à importer et gérer des données issues de BOFiP, lesquelles se présentent sous la forme de documents composés de deux fichiers complémentaires :  
- **data.html** : Contient le contenu principal au format HTML.  
- **document.xml** : Fournit les métadonnées au format XML (incluant les standards Dublin Core et les spécificités BOFiP).

Ces données seront ultérieurement consommées par un système RAG (Retrieval Augmented Generation) pour la vectorisation et l'alimentation d'un modèle de langage. La priorité est de disposer rapidement d'un corpus textuel complet associé à ses métadonnées.

## Justification du Choix de MySQL

### 1. Adaptation à la Modélisation des Données

- **Stockage Semi-Structuré** :  
  La modélisation retenue regroupe l'intégralité des informations (contenu HTML et métadonnées) dans une table unique. MySQL, à partir de la version 5.7, offre un support natif pour le type de données `JSON`, permettant ainsi de stocker les métadonnées en format flexible tout en conservant des colonnes classiques pour les données structurées.

- **Simplicité du Schéma** :  
  Notre modèle (MCD, MLD et MPD) se base sur une table unique, justifiée par le besoin de faciliter l'import, la gestion et l'extraction des données pour la vectorisation. MySQL permet de gérer efficacement ce schéma dénormalisé tout en offrant des fonctionnalités avancées pour l'interrogation (indexation, FULLTEXT, etc.).

### 2. Réponse aux Contraintes du Projet

- **Performance et Scalabilité** :  
  MySQL est reconnu pour sa robustesse et ses performances dans la gestion de grandes quantités de données. Son support pour les index, y compris les index FULLTEXT sur les colonnes textuelles, est un atout majeur pour l'extraction rapide des passages textuels, indispensable à notre phase de vectorisation.

- **Conformité RGPD** :  
  La centralisation des données dans une base unique permet de mieux contrôler l'accès et la suppression des informations personnelles. MySQL offre des mécanismes robustes de gestion des transactions et des permissions, facilitant ainsi le respect des exigences RGPD.

- **Simplicité d'Intégration** :  
  Le déploiement et la maintenance de MySQL sont largement documentés et supportés par une vaste communauté. Cette simplicité d'intégration réduit le temps de mise en œuvre, ce qui est crucial pour répondre rapidement aux besoins du projet et pour préparer l'intégration ultérieure dans un système RAG.

### 3. Contexte d'Utilisation RAG

- **Facilité d'Extraction et de Vectorisation** :  
  Le choix d'une base unique simplifie l'extraction du contenu textuel et des métadonnées pour la vectorisation. En effet, disposer de toutes les informations dans une seule table permet d'éviter des jointures complexes qui ralentiraient le traitement lors de l'indexation des passages pour la création des embeddings.

- **Flexibilité et Évolutivité** :  
  Le stockage des métadonnées en JSON offre une grande flexibilité pour adapter la structure des données en fonction des évolutions du projet sans nécessiter de refonte complète du schéma.

## Conclusion

MySQL est choisi pour ce projet parce qu'il s'aligne parfaitement avec notre modélisation des données semi-structurées et répond aux contraintes de performance, de simplicité et de conformité RGPD. La capacité de MySQL à gérer des données JSON, combinée à ses performances éprouvées et à sa simplicité d'intégration, en fait le SGBD idéal pour alimenter ultérieurement un système RAG tout en assurant une gestion efficace des données issues de BOFiP.
