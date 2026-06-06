# admin.py — Interface d'administration Django pour le RSVP Mariage
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html

from .models import Invite


# ─────────────────────────────────────────────
#  Filtre personnalisé : par boisson
# ─────────────────────────────────────────────

class BoissonFilter(admin.SimpleListFilter):
    title        = 'Boisson choisie'
    parameter_name = 'boisson'

    def lookups(self, request, model_admin):
        return Invite.BOISSON_CHOICES[1:]  # on retire le choix vide

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(choix_boisson=self.value())
        return queryset


# ─────────────────────────────────────────────
#  Configuration de l'admin Invite
# ─────────────────────────────────────────────

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):

    # Colonnes affichées dans la liste
    list_display = (
        'prenom', 'nom', 'code_invitation',
        'badge_statut', 'boisson_label', 'date_reponse'
    )

    # Filtres latéraux
    list_filter = ('statut_presence', BoissonFilter)

    # Champ de recherche
    search_fields = ('nom', 'prenom', 'code_invitation')

    # Tri par défaut
    ordering = ('nom', 'prenom')

    # Champs en lecture seule dans le formulaire
    readonly_fields = ('date_reponse',)

    # Organisation des champs du formulaire
    fieldsets = (
        ('Identité', {
            'fields': ('prenom', 'nom', 'code_invitation')
        }),
        ('Réponse', {
            'fields': ('statut_presence', 'choix_boisson', 'date_reponse')
        }),
    )

    # ── Colonnes enrichies ──

    @admin.display(description='Statut', ordering='statut_presence')
    def badge_statut(self, obj):
        """Affiche un badge coloré selon le statut."""
        couleurs = {
            'en_attente': ('#FFA500', '⏳ En attente'),
            'present':    ('#28a745', '✅ Présent'),
            'absent':     ('#dc3545', '❌ Absent'),
        }
        color, label = couleurs.get(obj.statut_presence, ('#999', obj.statut_presence))
        return format_html(
            '<span style="color:{};font-weight:bold">{}</span>', color, label
        )

    @admin.display(description='Boisson')
    def boisson_label(self, obj):
        """Affiche le libellé lisible de la boisson."""
        mapping = dict(Invite.BOISSON_CHOICES)
        return mapping.get(obj.choix_boisson, '—')

    # ── Vue de synthèse en pied de page ──

    def changelist_view(self, request, extra_context=None):
        """Ajoute les compteurs de boissons au bas de la liste."""
        extra_context = extra_context or {}

        # Compteurs globaux
        qs = self.get_queryset(request)
        extra_context['total_presents'] = qs.filter(statut_presence='present').count()
        extra_context['total_absents']  = qs.filter(statut_presence='absent').count()
        extra_context['total_attente']  = qs.filter(statut_presence='en_attente').count()

        # Compteurs par boisson (uniquement les présents)
        boissons = (
            qs.filter(statut_presence='present')
              .values('choix_boisson')
              .annotate(total=Count('choix_boisson'))
              .order_by('-total')
        )
        mapping = dict(Invite.BOISSON_CHOICES)
        extra_context['compteurs_boissons'] = [
            {'label': mapping.get(b['choix_boisson'], b['choix_boisson']), 'total': b['total']}
            for b in boissons if b['choix_boisson']
        ]

        return super().changelist_view(request, extra_context=extra_context)
