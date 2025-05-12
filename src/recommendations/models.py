from django.db import models
from patients.models import Patient

# Create your models here.

class Recommendation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    advice = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)