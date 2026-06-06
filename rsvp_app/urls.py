# urls.py — Routes de l'application RSVP Mariage
from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil : l'enveloppe + formulaire de connexion
    path('',              views.connexion,   name='connexion'),

    # Page de réponse RSVP (protégée par session)
    path('rsvp/',         views.rsvp,        name='rsvp'),

    # Page de confirmation après soumission
    path('confirmation/', views.confirmation, name='confirmation'),

    # Déconnexion / réinitialisation de session
    path('deconnexion/',  views.deconnexion,  name='deconnexion'),
]
