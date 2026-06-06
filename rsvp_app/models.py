# models.py — Modèle de données pour l'application RSVP Mariage
from django.db import models
from django.utils import timezone


class Invite(models.Model):
    """
    Représente un invité au mariage avec son statut de présence
    et son choix de boisson.
    """

    # --- Choix disponibles ---
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('present',    'Présent'),
        ('absent',     'Absent'),
    ]

    BOISSON_CHOICES = [
        ('',           '— Choisir —'),
        ('jus',        'Jus de fruit'),
        ('vin_rouge',  'Vin rouge'),
        ('vin_blanc',  'Vin blanc'),
        ('champagne',  'Champagne'),
        ('biere',      'Bière'),
        ('eau',        'Eau'),
    ]

    # --- Champs ---
    nom             = models.CharField(max_length=100, verbose_name="Nom de famille")
    prenom          = models.CharField(max_length=100, verbose_name="Prénom")
    code_invitation = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Code d'invitation"
    )
    statut_presence = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente',
        verbose_name="Statut de présence"
    )
    choix_boisson   = models.CharField(
        max_length=20,
        choices=BOISSON_CHOICES,
        blank=True,
        default='',
        verbose_name="Choix de boisson"
    )
    date_reponse    = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de réponse"
    )

    class Meta:
        verbose_name        = "Invité"
        verbose_name_plural = "Invités"
        ordering            = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom} [{self.code_invitation}]"

    def save(self, *args, **kwargs):
        """Normalise le nom et le prénom à la sauvegarde."""
        self.nom    = self.nom.strip().upper()
        self.prenom = self.prenom.strip().capitalize()
        super().save(*args, **kwargs)
