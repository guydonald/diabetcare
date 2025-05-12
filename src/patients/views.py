from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.contrib import messages
from .forms import TemporaryPatientForm, PatientForm
from .models import TemporaryPatient, Patient
from users.models import CustomUser

def temporary_patient_form_view(request):
    if request.method == 'POST':
        form = TemporaryPatientForm(request.POST)
        if form.is_valid():
            temp_patient = form.save()  # Enregistrer les données temporairement
            request.session["temp_patient_id"] = temp_patient.id  # Stocker l'ID en session
            return redirect('nutrition-form')  # Rediriger vers le formulaire de renseignement nutrition
    else:
        form = TemporaryPatientForm()
    
    return render(request, 'patients/form.html', {'form': form})

def finalize_registration_patient(request, user):
    """Migrer les données de TemporaryPatient vers Patient après l'inscription"""
    
    temp_patient_id = request.session.get("temp_patient_id")
    
    if temp_patient_id:
        try:
            temp_patient = TemporaryPatient.objects.get(id=temp_patient_id)

            # Vérifier si un Patient existe déjà pour cet utilisateur
            patient, created = Patient.objects.get_or_create(
                user=user,
                defaults={
                    "genre": temp_patient.genre,
                    "age_range": temp_patient.age_range,
                    "weight": temp_patient.weight,
                    "height": temp_patient.height,
                    "diabetes_type": temp_patient.diabetes_type,
                    "fasting_glucose": temp_patient.fasting_glucose,
                    "postprandial_glucose": temp_patient.postprandial_glucose,
                    "hypertension": temp_patient.completed,
                    "dyslipidemia": False,
                    "kidney_disease": False,
                    "obesity": False,
                    "completed": True,
                }
            )

            if created:
                temp_patient.delete()  # Supprimer les données temporaires si migration réussie
                del request.session["temp_patient_id"]
            else:
                print("Le profil Patient existe déjà, migration ignorée.")

        except TemporaryPatient.DoesNotExist:
            print("Aucune donnée temporaire trouvée.")

    return redirect("dashboard")

@login_required
def patient_step_one(request):
    """Vue qui enregistre ou met à jour les infos patient."""
    patient, created = Patient.objects.get_or_create(user=request.user)  # Création automatique si nécessaire

    form = PatientForm(instance=patient)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            new_patient = form.save(commit=False)
            new_patient.user = request.user
            new_patient.save()
            if new_patient.pk:  # S'assure que les données ont bien été enregistrées
                messages.success(request, "Votre profil patient a été mis à jour avec succès !")
            else:
                messages.error(request, "Une erreur est survenue lors de l'enregistrement.")
            return redirect("habitudes_step_one")
    return render(request, "patients/form_step_one.html", {"form": form})

@login_required
def patient_step_two(request):
    # Récupérer les données sauvegardées et afficher la prochaine étape
    return render(request, "patients/form_step_two.html")