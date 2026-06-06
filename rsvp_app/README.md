# 🥂 RSVP Mariage — Application Django
## Guide d'installation complet

---

## Structure du projet

```
mon_projet/
├── manage.py
├── mon_projet/
│   ├── settings.py
│   ├── urls.py (projet)
│   └── wsgi.py
└── rsvp_app/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── templates/
        └── rsvp_app/
            ├── connexion.html
            ├── rsvp.html
            └── confirmation.html
```

---

## 1. Création du projet Django

```bash
# Installer Django
pip install django

# Créer le projet
django-admin startproject mon_projet
cd mon_projet

# Créer l'application
python manage.py startapp rsvp_app
```

---

## 2. Configuration settings.py

```python
# mon_projet/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rsvp_app',   # ← Ajouter votre application
]

# Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,   # ← Important : cherche dans app/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Sessions (nécessaire pour la protection des vues)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 21600  # 6 heures en secondes

# Langue et fuseau horaire (à adapter)
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True
```

---

## 3. Configuration urls.py (projet)

```python
# mon_projet/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rsvp_app.urls')),  # ← Routes de l'application
]
```

---

## 4. Déploiement des fichiers

Copiez les fichiers fournis dans les emplacements suivants :

| Fichier fourni        | Destination                              |
|-----------------------|------------------------------------------|
| `models.py`           | `rsvp_app/models.py`                     |
| `views.py`            | `rsvp_app/views.py`                      |
| `urls.py`             | `rsvp_app/urls.py`                       |
| `admin.py`            | `rsvp_app/admin.py`                      |
| `connexion.html`      | `rsvp_app/templates/rsvp_app/connexion.html` |
| `rsvp.html`           | `rsvp_app/templates/rsvp_app/rsvp.html`  |
| `confirmation.html`   | `rsvp_app/templates/rsvp_app/confirmation.html` |

---

## 5. Migrations et base de données

```bash
# Créer les migrations
python manage.py makemigrations rsvp_app

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur pour l'administration
python manage.py createsuperuser
```

---

## 6. Ajouter des invités (via l'admin ou le shell)

### Via l'interface d'administration
```
http://127.0.0.1:8000/admin/
```

### Via le shell Django
```python
python manage.py shell

from rsvp_app.models import Invite

# Créer un invité
Invite.objects.create(
    nom='DUPONT',
    prenom='Marie',
    code_invitation='MRG-2025-001'
)

# Import en lot depuis une liste
invites = [
    {'nom': 'MARTIN',  'prenom': 'Jean',    'code_invitation': 'MRG-2025-002'},
    {'nom': 'BERNARD', 'prenom': 'Sophie',  'code_invitation': 'MRG-2025-003'},
    {'nom': 'THOMAS',  'prenom': 'Pierre',  'code_invitation': 'MRG-2025-004'},
]
for data in invites:
    Invite.objects.create(**data)

print(f"Total invités : {Invite.objects.count()}")
```

---

## 7. Lancement du serveur

```bash
python manage.py runserver
```

Application accessible sur : **http://127.0.0.1:8000/**

---

## 8. Résumé des URLs

| URL               | Vue          | Description                        |
|-------------------|--------------|------------------------------------|
| `/`               | connexion    | Page d'accueil — l'enveloppe       |
| `/rsvp/`          | rsvp         | Formulaire de réponse (protégé)    |
| `/confirmation/`  | confirmation | Page de remerciement               |
| `/deconnexion/`   | deconnexion  | Réinitialise la session            |
| `/admin/`         | admin Django | Interface d'administration         |

---

## 9. Fonctionnalités de l'administration

Accédez à `/admin/` pour :
- **Voir tous les invités** avec filtres par statut et par boisson
- **Compteurs automatiques** : nombre de présents, absents, en attente
- **Compteurs par boisson** en bas de la liste
- **Recherche** par nom, prénom ou code d'invitation
- **Badge coloré** selon le statut (vert, rouge, orange)

---

## 10. Logique de sécurité

- La page `/rsvp/` est **bloquée** sans session active → redirection vers `/`
- La comparaison nom/code est **insensible à la casse** (`.upper()` + `iexact`)
- Les espaces superflus sont **ignorés** (`.strip()`)
- Les sessions expirent après **6 heures**
- Le token CSRF Django protège tous les formulaires

---

## Thème visuel

| Élément         | Valeur CSS          |
|-----------------|---------------------|
| Fond principal  | `#080c10` (noir)    |
| Bleu ciel       | `#5baee3`           |
| Bleu clair      | `#a8d4f0`           |
| Or              | `#c9a84c`           |
| Or clair        | `#e8cf8a`           |
| Blanc crème     | `#f7f4ef`           |
| Police titre    | Cormorant Garamond  |
| Police corps    | Jost                |
