from django.db import models
from users.models import CustomUser

# Create your models here.

class Consultation(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_consultation = models.DateField(auto_now_add=True)

class MesureMedicale(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name="mesures")
    poids = models.FloatField()
    taille = models.FloatField()
    imc = models.FloatField(null=True, blank=True)
    glycemie_jeun = models.FloatField()
    hba1c = models.FloatField()
    cholesterol_hdl = models.FloatField()
    cholesterol_ldl = models.FloatField()

"""
class HealthRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    fasting_glucose = models.FloatField()
    postprandial_glucose = models.FloatField()
    complications = models.JSONField()
    additional_conditions = models.JSONField()  # Hypertension, Dyslipidemia, etc.
    created_at = models.DateTimeField(auto_now_add=True)

"""