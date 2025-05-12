from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from nutritions.models import TemporaryHabitudesAlimentaires, HabitudesAlimentaires
from nutritions.views import finalize_registration_nutrition
from activities.models import TemporaryActivityProfile, ActivityProfile
from activities.views import finalize_registration_activity
from patients.models import Patient
from patients.views import finalize_registration_patient

@receiver(user_signed_up)
def handle_user_signup(request, user, **kwargs):
    # Appelle tes fonctions ici après l'inscription
    finalize_registration_nutrition(request, user)
    finalize_registration_activity(request, user)
    finalize_registration_patient(request, user)
