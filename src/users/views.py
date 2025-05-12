from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.utils.translation import gettext as _
from django.contrib.auth import login, authenticate, get_backends
from django.utils.translation import activate
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from nutritions.models import TemporaryHabitudesAlimentaires, HabitudesAlimentaires
from nutritions.views import finalize_registration_nutrition
from activities.models import TemporaryActivityProfile, ActivityProfile
from activities.views import finalize_registration_activity
from patients.models import Patient
from patients.views import finalize_registration_patient
from .models import CustomUser
from .forms import UserRegistrationForm

def user_registration(request):
    """Vue pour gérer l'inscription standard et la migration des données temporaires"""
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # 🔹 Spécifier le backend pour éviter l'erreur
            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"

            login(request, user)  # Connecte l'utilisateur

            # 🔥 Appeler les différentes migrations après inscription
            finalize_registration_patient(request, user)
            finalize_registration_nutrition(request, user)
            finalize_registration_activity(request, user)

            return redirect("dashboard")  # Rediriger après migration des données
    
    else:
        form = UserRegistrationForm()
    
    return render(request, "users/registration.html", {"form": form})

@login_required
def dashboard(request):
    """Vue du tableau de bord après inscription"""
    patient = Patient.objects.filter(user=request.user).first()
    nutrition = HabitudesAlimentaires.objects.filter(patient=patient).first()
    activity = ActivityProfile.objects.filter(patient=patient).first()

    context = {
        "patient": patient,
        "nutrition": nutrition,
        "activity": activity,
    }

    return render(request, "users/dashboard.html", context)

def custom_login(request):
    user = authenticate(username=..., password=...)
    if user:
        # Mise à jour des infos de sécurité
        user.last_ip = request.META.get('REMOTE_ADDR')
        user.last_user_agent = request.META.get('HTTP_USER_AGENT')
        user.save()

        # Initialisation de la session
        request.session['auth_token'] = str(user.security_token)
        login(request, user)

def home(request):
    context = {
        'welcome_message': _("Bienvenue sur NutriAfrica !"),
    }
    return render(request, 'accueil.html', context)

def set_language(request):
    if request.method == "POST":
        lang = request.POST.get("language", "fr")  # Récupère la langue sélectionnée
        activate(lang)
        request.session["django_language"] = lang
        return JsonResponse({"success": True, "language": lang})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def user_summary(request):
    """Vue qui affiche le résumé complet des informations du patient."""
    patient = get_object_or_404(Patient, user=request.user)  # Correction ici

    # Sécurisation des données pour éviter les injections XSS
    patient_data = {key: escape(str(value)) for key, value in patient.__dict__.items()}
    nutrition_data = HabitudesAlimentaires.objects.filter(patient=patient).first()
    activity_data = ActivityProfile.objects.filter(patient=patient).first()

    return render(request, "users/patient_summary.html", {
        "patient": patient_data,
        "nutrition": nutrition_data,
        "activity": activity_data,
    })

def is_admin(user):
    return user.is_admin  # Vérifie si l'utilisateur est un administrateur

@login_required
@user_passes_test(is_admin)
def manage_patients(request):
    """Vue permettant à l'admin de gérer les patients et modifier leurs informations."""
    patients = Patient.objects.all()

    patients_details = []
    for patient in patients:
        nutrition = HabitudesAlimentaires.objects.filter(patient=patient).first()
        activity = ActivityProfile.objects.filter(patient=patient).first()
        patients_details.append({
            "patient": patient,
            "nutrition": nutrition,
            "activity": activity
        })

    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        patient = get_object_or_404(Patient, id=patient_id)

        # Modifier les informations générales du patient
        if "modify_patient" in request.POST:
            try:
                patient.genre = request.POST.get("genre")
                patient.age_range = request.POST.get("age_range")
                patient.diabetes_type = request.POST.get("diabetes_type")
                patient.weight = float(request.POST.get("weight"))
                patient.height = float(request.POST.get("height"))
                patient.save()
                messages.success(request, f"Les informations du patient {patient.user.email} ont été mises à jour avec succès !")
            except ValueError:
                messages.error(request, "Erreur : Veuillez entrer des valeurs valides pour le poids et la taille.")

        # Modifier les habitudes alimentaires
        elif "modify_nutrition" in request.POST:
            nutrition = HabitudesAlimentaires.objects.filter(patient=patient).first()
            if nutrition:
                nutrition.frequence_repas = request.POST.get("frequence_repas")
                nutrition.portion = request.POST.get("portion")
                nutrition.eau_consommee = request.POST.get("eau_consommee")
                nutrition.save()
                messages.success(request, f"Les habitudes alimentaires de {patient.user.email} ont été mises à jour !")

        # Modifier l’activité physique
        elif "modify_activity" in request.POST:
            activity = ActivityProfile.objects.filter(patient=patient).first()
            if activity:
                activity.physical_activity_duration = request.POST.get("physical_activity_duration")
                activity.physical_activity_frequency = request.POST.get("physical_activity_frequency")
                activity.intensity_level = request.POST.get("intensity_level")
                activity.sleep_hours = request.POST.get("sleep_hours")
                activity.stress_level = request.POST.get("stress_level")
                activity.save()
                messages.success(request, f"L’activité physique de {patient.user.email} a été mise à jour !")

    return render(request, "users/manage_patients.html", {"patients_details": patients_details})



@login_required
@user_passes_test(is_admin)
def patient_details(request, patient_id):
    """Vue pour afficher les détails d'un patient et permettre l'envoi d'email."""
    patient = get_object_or_404(Patient, id=patient_id)
    nutrition = HabitudesAlimentaires.objects.filter(patient=patient).first()
    activity = ActivityProfile.objects.filter(patient=patient).first()
    
    if request.method == "POST":
        subject = "Conseils Santé Personnalisés"
        message = request.POST.get("message")
        from_email = "admin@site.com"  # Remplace par ton email d'expéditeur
        recipient_list = [patient.user.email]

        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, f"Email envoyé à {patient.user.email} avec succès !")
        return render(request, "users/patient_details.html", {"patient": patient})

    return render(request, "users/patient_details.html", {"patient": patient, 'nutrition': nutrition, 'activity': activity})
