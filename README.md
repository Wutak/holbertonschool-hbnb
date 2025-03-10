### Explication du Diagramme de Classes

Le diagramme de classes représente un système de gestion d’avis pour des lieux (hôtels, restaurants, etc.). Il comprend quatre entités principales : **User**, **Review**, **Place**, et **Amenity**. Chaque classe possède ses propres attributs et méthodes, et leurs relations définissent la structure du système.

---

### 1. Classe **User**

#### Rôle :
L'entité **User** représente un utilisateur du système qui peut s'inscrire, se connecter, gérer son compte, et laisser des avis sur des lieux.

#### Attributs clés :
- `uuid` : Identifiant unique de l’utilisateur (privé).
- `firstname` & `lastname` : Prénom et nom de l’utilisateur.
- `email` : Adresse e-mail pour l’identification.
- `admin` : Booléen indiquant si l’utilisateur est administrateur (privé).
- `password` : Mot de passe de l’utilisateur (privé).
- `date_of_creation` & `date_of_update` : Dates de création et de mise à jour du compte.

#### Méthodes principales :
- `register()` : Permet l’inscription d’un nouvel utilisateur.
- `login()` / `logout()` : Gestion de l’authentification.
- `delete()` : Supprime le compte utilisateur.
- `get_date_of_creation()` & `get_date_of_update()` : Récupèrent les dates de création et mise à jour.

---

### 2. Classe **Review**

#### Rôle :
Cette entité représente un avis laissé par un utilisateur sur un lieu spécifique. Chaque avis est associé à un utilisateur et à un lieu.

#### Attributs clés :
- `uuid` : Identifiant unique de l’avis (privé).
- `user` : Référence à l’utilisateur qui a écrit l’avis.
- `place` : Référence au lieu concerné.
- `rating` : Note attribuée (ex. : 1 à 5 étoiles).
- `comment` : Commentaire laissé par l’utilisateur.
- `date_of_review` & `date_of_update` : Dates de publication et de mise à jour de l’avis.

#### Méthodes principales :
- `write_review()` : Création d’un avis.
- `delete()` : Suppression de l’avis.
- `edit()` : Modification de l’avis.
- `get_reviews_by_place()` & `get_reviews_by_user()` : Récupération des avis en fonction du lieu ou de l’utilisateur.
- `get_date_of_review()` & `get_date_of_creation()` : Gestion des dates.

---

### 3. Classe **Place**

#### Rôle :
Représente un lieu qui peut être évalué par les utilisateurs. Chaque lieu a un propriétaire et des caractéristiques spécifiques.

#### Attributs clés :
- `uuid` : Identifiant unique du lieu (privé).
- `title` : Nom du lieu.
- `latitude` & `longitude` : Coordonnées géographiques du lieu.
- `price` : Coût estimé d’un séjour ou service proposé.
- `owner` : Identifiant du propriétaire du lieu.
- `description` : Brève présentation du lieu.
- `average_rating` : Note moyenne basée sur les avis.
- `amenities` : Liste des commodités disponibles.
- `date_of_creation` & `date_of_update` : Dates de création et de modification.

#### Méthodes principales :
- `create_place()` / `update_place()` / `delete_place()` : Gestion du cycle de vie du lieu.
- `get_available_dates()` : Récupère les dates de disponibilité.
- `calculate_price()` : Calcule le coût d’une réservation.
- `calculate_average_rating()` : Met à jour la note moyenne.
- `get_amenities()` / `add_amenity()` / `remove_amenity()` : Gestion des commodités.
- `get_date_of_creation()` & `get_date_of_update()` : Gestion des dates.

---

### 4. Classe **Amenity**

#### Rôle :
Cette entité représente une commodité ou un service offert par un lieu (ex. : Wi-Fi, piscine, parking, etc.).

#### Attributs clés :
- `uuid` : Identifiant unique de la commodité (privé).
- `name` : Nom de la commodité.
- `description` : Brève description.
- `date_of_creation` & `date_of_update` : Dates de gestion.

#### Méthodes principales :
- `create_amenity()` / `update_amenity()` / `delete_amenity()` : Gestion des commodités.
- `get_all_amenity()` : Liste toutes les commodités disponibles.
- `get_date_of_creation()` & `get_date_of_update()` : Gestion des dates.

---

### Relations entre les Entités

1. **User → Review** :
   - Un utilisateur peut écrire plusieurs avis.
   - Chaque avis appartient à un seul utilisateur.

2. **Review → Place** :
   - Chaque avis est associé à un lieu spécifique.
   - Un lieu peut avoir plusieurs avis.

3. **Review → User** :
   - Lien bidirectionnel confirmant que les avis sont liés aux utilisateurs.

4. **User → Place** :
   - Un utilisateur peut être propriétaire d’un ou plusieurs lieux.
   - Cette relation permet la gestion des lieux par les utilisateurs.

5. **Amenity *-- Place** :
   - Une commodité peut être associée à plusieurs lieux.
   - Un lieu peut proposer plusieurs commodités.
   - Cette relation facilite l’ajout ou la suppression de commodités pour un lieu donné.

---

### Contribution à la Logique du Système

Ce modèle de données définit une application permettant aux utilisateurs de gérer des lieux, de laisser des avis, et d’interagir avec les commodités offertes. Les relations entre les classes assurent la cohérence des données et permettent des fonctionnalités comme :

- **Gestion des utilisateurs** (inscription, connexion, suppression de compte).
- **Évaluation des lieux** (ajout, modification et suppression d’avis).
- **Gestion des lieux** (création, modification, suppression, notation).
- **Gestion des commodités** (ajout/suppression de services offerts).
- **Calcul automatique des évaluations moyennes des lieux**.

En structurant ainsi les classes et leurs relations, le système assure une bonne organisation des données et une évolutivité permettant d’ajouter de nouvelles fonctionnalités facilement.

## Diagramme des classes
![Screenshot 2025-02-15 170706](https://github.com/user-attachments/assets/6e1e011c-babb-4b01-81b6-04e8027d93b6)
```
classDiagram
direction TB
    class User {
	    -uuid : str
	    +firstname : str
	    +lastname : str
	    +email : str
	    +admin : bool
	    -password : str
	    +date_of_creation : int
	    +date_of_update : int
	    register()
	    login()
	    logout()
	    delete()
	    get_date_of_creation()
	    get_date_of_update()
    }
    class Review {
	    -uuid : str
	    +user : str
	    +place : str
	    +rating : int
	    +comment : str
	    +date_of_review : int
	    +date_of_update : int
	    write_review()
	    delete()
	    edit()
	    get_reviews_by_place()
	    get_reviews_by_user()
	    get_date_of_review()
	    get_date_of_creation()
    }
    class Place {
	    - uuid : str
	    +title : str
	    +latitude : float
	    +longitude : float
	    +price : int
	    +owner : str
	    +description : str
	    +average_rating : int
	    +amenities : List[Amenity]
	    +date_of_creation : int
	    +date_of_update : int
	    create_place()
	    update_place()
	    delete_place()
	    get_available_dates()
	    calculate_price()
	    calculate_average_rating()
	    get_amenities()
	    add_amenity()
	    remove_amenity()
	    get_date_of_creation()
	    get_date_of_update()
    }
    class Amenity {
	    -uuid : str
	    +name : str
	    +description : str
	    +date_of_creation : int
	    +date_of_update : int
	    create_amenity()
	    update_amenity()
	    delete_amenity()
	    get_all_amenity()
	    get_date_of_creation()
	    get_date_of_update()
    }
    User "1" --> "N" Review (un utilisateur → plusieurs avis)
    Review "N" --> "1" Place (plusieurs avis → un lieu)
    User "1" --> "N" Place (un utilisateur → plusieurs lieux)
    Amenity "*--*" Place (plusieurs commodités peuvent être associées à plusieurs lieux)
