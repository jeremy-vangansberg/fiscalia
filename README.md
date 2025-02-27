# Fiscalia

## Description
Fiscalia est un projet visant à développer un Large Language Model (LLM) spécialisé dans le domaine de la fiscalité. L'objectif est de créer un assistant intelligent capable de répondre avec précision aux questions fiscales, en s'appuyant sur une base de connaissances spécialisée et mise à jour.

## Sources de Données
Le projet s'appuie principalement sur les données open source du Bulletin Officiel des Finances Publiques (BOFiP), qui constitue la documentation officielle de l'administration fiscale française. Ces données sont :
- Publiques et accessibles à tous
- Régulièrement mises à jour
- Faisant autorité en matière fiscale
- Structurées par thématiques fiscales

## Objectifs
- Créer un LLM spécialisé en fiscalité
- Fournir des réponses précises et à jour sur les questions fiscales
- Assurer la traçabilité des sources utilisées
- Maintenir une base de connaissances fiscales actualisée
- Faciliter l'accès et la compréhension du BOFiP

## Modules

### Data Collection
Module de collecte de données fiscales depuis diverses sources :
- Documentation officielle
- BOFiP (source principale)
- Textes de loi
- Jurisprudence
- Articles spécialisés
[Plus de détails](./data_collection/README.md)

### Machine Learning
Module d'entraînement et d'optimisation du LLM :
- Fine-tuning sur les données fiscales
- Évaluation des performances
- Amélioration continue du modèle
- Validation des réponses avec les sources BOFiP
[Plus de détails](./machine_learning/README.md)

## Installation
Chaque module utilise Poetry pour la gestion des dépendances. Voir les README respectifs pour les instructions d'installation spécifiques.

## Contribution
Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour les détails.

## Licence
Ce projet est sous Apache 2.0 Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Note Légale
Ce LLM est conçu comme un outil d'aide et d'information. Il ne remplace pas l'expertise d'un professionnel de la fiscalité. Les réponses fournies ne constituent pas un conseil fiscal officiel.

## Mentions Légales
Les données utilisées dans ce projet proviennent du Bulletin Officiel des Finances Publiques (BOFiP), une ressource publique mise à disposition par la Direction Générale des Finances Publiques. L'utilisation de ces données est conforme à leur statut de données publiques.