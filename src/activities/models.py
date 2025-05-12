from django.db import models
from patients.models import Patient

# Create your models here.

CHOIX_ACTIVITÉ = [
    ("none", "Je ne fais pas de sport"),
    ("walking", "Marche"),
    ("running", "Course à pied"),
    ("cycling", "Cyclisme"),
    ("swimming", "Natation"),
    ("gym", "Salle de sport"),
]

class ActivityProfile(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="activities")
    
    # Type d’activité physique (inclut une option "Je ne fais pas de sport")
    activity_type = models.JSONField(default=dict, verbose_name="Types d'activités pratiquées")

    # Durée de l’activité physique (si le patient est sédentaire, mettre 'none')
    physical_activity_duration = models.CharField(
        choices=[
            ('none', 'Aucune activité physique'),
            ('less_30min', 'Moins de 30 min'), 
            ('30-60min', '30-60 min'), 
            ('more_60min', 'Plus de 60 min')
        ],
        max_length=20, verbose_name="Durée de l'activité physique"
    )

    # Fréquence des séances (inclut une option "Je ne fais pas de sport")
    physical_activity_frequency = models.CharField(
        choices=[
            ('none', 'Jamais'),
            ('once', 'Une fois par semaine'), 
            ('twice', 'Deux fois par semaine'), 
            ('thrice', 'Trois fois par semaine'), 
            ('more_than_thrice', 'Plus de trois fois')
        ],
        max_length=20, verbose_name="Fréquence de l'activité physique"
    )

    # Niveau d’intensité (remplacé par 'none' si aucun sport)
    intensity_level = models.CharField(
        choices=[('none', 'Non applicable'), ('low', 'Faible'), ('moderate', 'Modéré'), ('high', 'Élevé')],
        max_length=10, verbose_name="Niveau d’intensité de l'activité"
    )

    # Heures de sommeil
    sleep_hours = models.CharField(
        choices=[('<5', 'Moins de 5 heures'), ('5-6', '5-6 heures'), ('7-8', '7-8 heures'), ('>8', 'Plus de 8 heures')],
        max_length=10, verbose_name="Durée du sommeil"
    )

    # Niveau de stress
    stress_level = models.CharField(
        choices=[('always', 'Tout le temps'), ('sometimes', 'Parfois'), ('rarely', 'Rarement'), ('never', 'Jamais')],
        max_length=20, verbose_name="Niveau de stress"
    )

    def __str__(self):
        return f"Activité physique de {self.patient.user.email}"

class TemporaryActivityProfile(models.Model):
    """Stocke temporairement les réponses du formulaire activité physique avant inscription"""
    session_id = models.CharField(max_length=255, verbose_name="ID de session")

    activity_type = models.JSONField(default=dict, verbose_name="Types d'activités pratiquées")
    
    physical_activity_duration = models.CharField(
        choices=[
            ('none', 'Aucune activité physique'),
            ('less_30min', 'Moins de 30 min'), 
            ('30-60min', '30-60 min'), 
            ('more_60min', 'Plus de 60 min')
        ],
        max_length=20, verbose_name="Durée de l'activité physique"
    )

    physical_activity_frequency = models.CharField(
        choices=[
            ('none', 'Jamais'),
            ('once', 'Une fois par semaine'), 
            ('twice', 'Deux fois par semaine'), 
            ('thrice', 'Trois fois par semaine'), 
            ('more_than_thrice', 'Plus de trois fois')
        ],
        max_length=20, verbose_name="Fréquence de l'activité physique"
    )

    intensity_level = models.CharField(
        choices=[('none', 'Non applicable'), ('low', 'Faible'), ('moderate', 'Modéré'), ('high', 'Élevé')],
        max_length=10, verbose_name="Niveau d’intensité de l'activité"
    )

    sleep_hours = models.CharField(
        choices=[('<5', 'Moins de 5 heures'), ('5-6', '5-6 heures'), ('7-8', '7-8 heures'), ('>8', 'Plus de 8 heures')],
        max_length=10, verbose_name="Durée du sommeil"
    )

    stress_level = models.CharField(
        choices=[('always', 'Tout le temps'), ('sometimes', 'Parfois'), ('rarely', 'Rarement'), ('never', 'Jamais')],
        max_length=20, verbose_name="Niveau de stress"
    )

    def __str__(self):
        return f"Données temporaires activité physique - Session {self.session_id}"