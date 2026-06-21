# views.py — Logique métier de l'application RSVP Mariage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages

from .models import Invite


# ─────────────────────────────────────────────
#  HELPER : protection de session
# ─────────────────────────────────────────────

def _get_invite_depuis_session(request):
    """
    Retourne l'objet Invite stocké en session, ou None si inexistant.
    Utilisé pour protéger les vues réservées aux invités connectés.
    """
    invite_id = request.session.get('invite_id')
    if not invite_id:
        return None
    try:
        return Invite.objects.get(pk=invite_id)
    except Invite.DoesNotExist:
        # Nettoyage d'une session corrompue
        request.session.flush()
        return None


# ─────────────────────────────────────────────
#  VUE 1 : Page de connexion (l'enveloppe)
# ─────────────────────────────────────────────

def connexion(request):
    """
    Affiche l'enveloppe animée et gère l'authentification
    via le couple (Nom de famille + Code d'invitation).

    Tolérances :
      - Espaces superflus ignorés (.strip())
      - Insensible à la casse (.upper() / .lower())
    """

    # Si déjà connecté → rediriger directement vers le RSVP
    if _get_invite_depuis_session(request):
        return redirect('rsvp')

    if request.method == 'POST':
        nom_saisi  = request.POST.get('nom', '').strip().upper()
        code_saisi = request.POST.get('code_invitation', '').strip().upper()

        if not nom_saisi or not code_saisi:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'rsvp_app/connexion.html')

        try:
            # Recherche insensible à la casse pour le code
            invite = Invite.objects.get(
                nom__iexact=nom_saisi,
                code_invitation__iexact=code_saisi
            )
            # Ouverture de session
            request.session['invite_id'] = invite.pk
            request.session.set_expiry(3600 * 6)  # 6 heures
            return redirect('rsvp')

        except Invite.DoesNotExist:
            messages.error(
                request,
                "Nom ou code d'invitation incorrect. Veuillez vérifier votre carton."
            )

    return render(request, 'rsvp_app/connexion.html')


# ─────────────────────────────────────────────
#  VUE 2 : Page RSVP (la réponse)
# ─────────────────────────────────────────────

def rsvp(request):
    """
    Permet à l'invité connecté de confirmer sa présence
    et de choisir une boisson s'il est présent.
    Accès bloqué si aucune session active.
    """

    invite = _get_invite_depuis_session(request)
    if not invite:
        messages.error(request, "Veuillez vous identifier pour accéder à cette page.")
        return redirect('connexion')

    if request.method == 'POST':
        statut   = request.POST.get('statut_presence', '').strip()
        boisson  = request.POST.get('choix_boisson', '').strip()

        # Validation basique du statut
        if statut not in ('present', 'absent'):
            messages.error(request, "Choix de présence invalide.")
            return render(request, 'rsvp_app/rsvp.html', {'invite': invite})

        invite.statut_presence = statut
        invite.date_reponse    = timezone.now()

        # Boisson uniquement si présent
        if statut == 'present':
            invite.choix_boisson = boisson if boisson else ''
        else:
            invite.choix_boisson = ''

        invite.save()
        return redirect('confirmation')

    return render(request, 'rsvp_app/rsvp.html', {'invite': invite})
def invitation(request):
    return render(request, 'rsvp_app/invitation.html')


# ─────────────────────────────────────────────
#  VUE 3 : Page de confirmation
# ─────────────────────────────────────────────

def confirmation(request):
    """
    Page de remerciement affichée après la soumission du RSVP.
    """
    invite = _get_invite_depuis_session(request)
    if not invite:
        return redirect('connexion')

    return render(request, 'rsvp_app/confirmation.html', {'invite': invite})


# ─────────────────────────────────────────────
#  VUE 4 : Déconnexion
# ─────────────────────────────────────────────

def deconnexion(request):
    """Vide la session et redirige vers la connexion."""
    request.session.flush()
    return redirect('connexion')

