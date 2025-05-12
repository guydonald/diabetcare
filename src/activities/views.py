from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.html import escape

from .forms import TemporaryActivityProfileForm, ActivityProfileForm
from .models import TemporaryActivityProfile, ActivityProfile
from patients.models import Patient

# Create your views here.

def activity_form_view(request):
    """Vue qui affiche le formulaire activité physique et stocke les réponses temporairement"""
    if request.method == 'POST':
        form = TemporaryActivityProfileForm(request.POST)
        if form.is_valid():
            activity_data = form.cleaned_data

            # Stocker les réponses en session Django
            request.session['activity_data'] = activity_data

            return redirect('account_signup')  # ✅ Vue d'inscription fournie par allauth
    else:
        form = TemporaryActivityProfileForm()
    
    return render(request, 'activities/activity_form.html', {'form': form})

def finalize_registration_activity(request, user):
    """Migration des données d'activité physique après inscription"""
    patient = Patient.objects.get(user=user)
    temp_activity = request.session.get("activity_data")
    print("Données activité récupérées :", temp_activity)

    if temp_activity:
        ActivityProfile.objects.create(
            patient=patient,
            activity_type=temp_activity["activity_type"],
            physical_activity_duration=temp_activity["physical_activity_duration"],
            physical_activity_frequency=temp_activity["physical_activity_frequency"],
            intensity_level=temp_activity["intensity_level"],
            sleep_hours=temp_activity["sleep_hours"],
            stress_level=temp_activity["stress_level"]
        )
        del request.session["activity_data"]

    return patient

@login_required
def activity_step_one(request):
    patient = get_object_or_404(Patient, user=request.user)
    activity_profile = patient.activities.first()  # Suppose un seul profil d'activité

    form = ActivityProfileForm(instance=activity_profile)
    if request.method == "POST":
        form = ActivityProfileForm(request.POST, instance=activity_profile)
        if form.is_valid():
            new_activity = form.save(commit=False)
            
            # Escape sur les champs texte
            new_activity.physical_activity_duration = escape(new_activity.physical_activity_duration)
            new_activity.physical_activity_frequency = escape(new_activity.physical_activity_frequency)
            new_activity.intensity_level = escape(new_activity.intensity_level)
            new_activity.sleep_hours = escape(new_activity.sleep_hours)
            new_activity.stress_level = escape(new_activity.stress_level)
            
            new_activity.patient = patient
            new_activity.save()
            return redirect("user_summary")
    return render(request, "activities/activity_step_one.html", {"form": form})
