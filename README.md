# Analyse de l'Employabilité Data Science

![Dashboard Power BI](docs/images/employablité_data_powerbi.png)

Ce projet vise à analyser le marché de l'emploi en Data Science en France à travers la collecte, le traitement et la visualisation de données d'offres d'emploi.

## Objectifs

*   **Collecte de données** : Scraping automatisé d'offres d'emploi (Welcome to the Jungle, APEC, etc.).
*   **Traitement** : Nettoyage, structuration et enrichissement des données.
*   **Analyse** : Visualisation interactive via Power BI pour identifier les tendances (salaires, compétences, localisation, types de contrats).

## Setup

Créer API France Travail [ici](https://francetravail.io/inscription)

Enlever le .exemple sur le fichier .env.exemple et y insérer vos clés API

Installer les dépendances Python suivantes :

```bash
pip install pandas requests python-dotenv selenium webdriver-manager matplotlib wordcloud beautifulsoup4
```

Mettre à jour Les `KEYWORDS` dans les scrapers

Lancer Main.py !

PS : Le scraping sur APEC et WTTJ est normalement interdit par leur T&C donc il ne faut pas baisser le délai entre chaque requête au risque que votre IP soit bloquée

## Auteurs

**Liza Bérénice Makani**
Étudiante Ingénieure - ESIEA (IA & Data Science)

**Sunnier**
Étudiant en cybersécurité