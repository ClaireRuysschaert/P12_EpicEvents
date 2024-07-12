# Projet 12 Openclassrooms - Développez une architecture backend sécurisée avec Python et SQL

L'objectif est de développer un CRM sécurisée à l'entreprise Epic Events qui organise des événements pour ses clients.

## Fonctionnalités

Le but est de collecter et traiter les données des clients et des événements organisés par l'entreprise via une base de données, tout en facilitant la communication entre les différents départements de l'entreprise.

La gestion est assurée par trois départements (commercial, support et management).

Les commerciaux prospectent les clients, créent et mettent à jour leurs profils sur la plateforme. Lorsqu'un client souhaite organiser un événement, un collaborateur du département management crée un contrat et l'associe au client.

Le commercial pourra alors créer l'événement sur la plateforme et le département management désigne un membre du département support responsable de l'organisation et du déroulement de l'événement.

## Technologies utilisées

Pour le développement de ce projet, plusieurs technologies et bibliothèques ont été utilisées afin de garantir une architecture backend sécurisée et performante :
- **SQLAlchemy** : Un ORM (Object-Relational Mapping) pour Python qui facilite les interactions avec la base de données PostgreSQL en permettant de manipuler les données comme des objets Python.
- **PostgreSQL** : Un système de gestion de base de données relationnelle robuste et performant, utilisé pour stocker et gérer les données des clients et des événements.
- **Click** : Une bibliothèque Python utilisée pour créer des interfaces en ligne de commande (CLI) simples et composables, facilitant ainsi l'interaction avec le système.
- **Argon2** : Un algorithme de hachage sécurisé utilisé pour le stockage des mots de passe, garantissant une protection renforcée contre les attaques par force brute.
- **JWT (JSON Web Tokens)** : Une méthode standard pour sécuriser les échanges de données entre deux parties, utilisée pour l'authentification et l'autorisation des utilisateurs.
- **PyJWT** : Une bibliothèque Python permettant de travailler facilement avec les JSON Web Tokens pour la gestion des sessions utilisateur.
- **Flake8** : Un outil de vérification de code Python qui assure le respect des conventions de style et détecte les erreurs potentielles dans le code.
- **isort** : Un outil qui trie automatiquement les importations dans les fichiers Python, améliorant ainsi la lisibilité et l'organisation du code.
- **Black** : Un formateur de code Python qui applique des règles de style strictes pour garantir un code uniforme et lisible.
- **unittest** : Le module de test intégré de Python, utilisé pour écrire et exécuter des tests unitaires afin de garantir la fiabilité et la robustesse du code.
- **Sentry** : Une plateforme de surveillance des erreurs qui permet de suivre et de corriger les erreurs en temps réel, améliorant ainsi la stabilité et la maintenance de l'application.

## Installation 
- Install Python 3.10. Launch the console and, in the folder of your choice, clone this repository :
```
git clone https://github.com/ClaireRuysschaert/P12_EpicEvents.git
```

- In the folder, create and activate a new virtual environment:
```
(linux)
python3 -m venv .venv
source .venv/bin/activate
(windows) 
python -m venv .venv
.\.venv\Scripts\activate
```

- Then, install the required packages :
```
pip install -r requirements.txt
```

- Créer un fichier .env avec ces clefs :
```
PGPASSWORD (admin password)
PGUSER (admin user)
PGHOST (host)
PGPORT (port)
PGDATABASE (nom de la base)
SECRET_KEY (secret key for jwt)
ALGORITHM (algorithm for jwt)
SENTRY_DSN (sentry dsn)
```

Il vous sera ensuite demandé de remplir les valeurs associées avant de pouvoir installer la base de données. 
```
psql -U your_username -d your_database -f initdb.sql
```

- Pour lancer l'application:
```
python run.py
```


## Tests

Pour lancer les tests:
```
python -m unittest discover -s tests
```

Pour obtenir la couverture des tests:
coverage run -m unittest discover -s tests
```
coverage report 
```

Pour afficher les détails sur navigateur, lancer la commande ci-dessous puis ouvrir le fichier dans htmlcov/index.html: 
```
coverage html
```
