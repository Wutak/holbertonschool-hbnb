### Hbnb part2
## Aperçu du Projet

Le projet HBnB est une application basée sur Flask qui utilise une structure modulaire et organisée pour faciliter le développement et l'évolution.
Cette application est conçue pour intégrer des points de terminaison d'API, gérer des objets via un référentiel en mémoire et mettre en œuvre le modèle de façade pour communiquer entre les différentes couches
```
hbnb/
├── app/                        # Contient le code principal de l'application
│   ├── __init__.py             # Initialisation de l'application Flask
│   ├── api/                    # Points de terminaison de l'API
│   │   ├── __init__.py         
│   │   ├── v1/                 # Version 1 de l'API
│   │       ├── __init__.py
│   │       ├── users.py        # Point de terminaison de l'API pour les utilisateurs
│   │       ├── places.py       # Point de terminaison de l'API pour les lieux
│   │       ├── reviews.py      # Point de terminaison de l'API pour les avis
│   │       ├── amenities.py    # Point de terminaison de l'API pour les commodités
│   ├── models/                 # Classes de logique métier
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/               # Implémentation du modèle Façade
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/            # Référentiel en mémoire
│       ├── __init__.py
│       ├── repository.py
├── run.py                      # Point d'entrée pour exécuter l'application Flask
├── config.py                   # Configuration des variables d'environnement et des paramètres
├── requirements.txt            # Packages Python nécessaires au projet
├── README.md                   # Aperçu du projet (ce fichier)
```
## Description des fichiers :
# app/ : Contient le code principal de l'application.

\\init\\.py : Fichier d'initialisation pour créer l'application Flask.

api/ : Répertoire pour les points de terminaison de l'API.

\\init\\.py : Fichier d'initialisation pour l'API.

v1/ : Répertoire pour la version 1 de l'API.

\\init\\.py : Fichier d'initialisation pour la version 1 de l'API.

users.py : Points de terminaison de l'API pour les utilisateurs.

places.py : Points de terminaison de l'API pour les lieux.

reviews.py : Points de terminaison de l'API pour les avis.

amenities.py : Points de terminaison de l'API pour les commodités.

# models/ : Répertoire pour les classes de logique métier.

\\init\\.py : Fichier d'initialisation pour les modèles.

user.py : Modèle de la logique métier pour les utilisateurs.

place.py : Modèle de la logique métier pour les lieux.

review.py : Modèle de la logique métier pour les avis.

amenity.py : Modèle de la logique métier pour les commodités.

# services/ : Répertoire pour l'implémentation du modèle Façade.

\\init\\.py : Fichier d'initialisation pour les services.

facade.py : Implémentation du modèle Façade pour gérer l'interaction entre les couches.

# persistence/ : Répertoire pour le référentiel en mémoire.

\\init\\.py : Fichier d'initialisation pour la persistance.

repository.py : Référentiel en mémoire pour gérer le stockage et la validation des objets.

run.py : Point d'entrée pour exécuter l'application Flask.

config.py : Configuration des variables d'environnement et des paramètres de l'application.

requirements.txt : Liste des packages Python nécessaires au projet.

README.md : Fichier contenant un aperçu du projet, des instructions d'installation et d'exécution.

---

# Business Logic Layer
La couche de logique métier est implémentée dans app/services/.

Elle définit comment les entités interagissent et applique les règles métier.

### Entités et responsabilités
| Entité | Description |
|--------|-------------|
| `Place` | Représente un lieu. |
| `Amenity` | Représente une commodité associée à un lieu. |
| `Review` | Représente un avis laissé par un utilisateur sur un lieu. |
| `User` | Représente un utilisateur qui peut être propriétaire d'un lieu ou laisser un avis. |

## Exemples d'Utilisation

### Créer un Lieu
```python
from app.models.user import User
from app.models.place import Place

# Création d'un propriétaire
owner = user(first_name="Alice", last_name="Smith", email="alice.smith@example.com")

# Création d'un lieu
place = Place(
    title="Cozy Apartment",
    description="Un bel endroit pour séjourner",
    price=100,
    latitude=37.7749,
    longitude=-122.4194,
    owner=owner
)

print(place)
```

### Ajouter une Commodité à un Lieu
```python
from app.models.amenity import Amenity

# Création d'une commodité
wifi = Amenity(name="Wi-Fi")

# Ajout de la commodité au lieu
place.add_amenity(wifi)

print(place.get_amenities())  # Liste des commodités associées
```

### Ajouter un Avis à un Lieu
```python
from app.models.amenity import Amenity

# Création d'une commodité
wifi = Amenity(name="Wi-Fi")

# Ajout de la commodité au lieu
place.add_amenity(wifi)

print(place.get_amenities())  # Liste des commodités associées
```

---
# Installation des Dépendances

Pour installer les dépendances nécessaires au projet, exécutez la commande suivante :
```
pip install -r requirements.txt
```
# Exécution de l'Application
Pour exécuter l'application Flask, utilisez la commande suivante :
```
python3 run.py
```

