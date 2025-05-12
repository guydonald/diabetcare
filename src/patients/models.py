from django.db import models
from users.models import CustomUser

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="patient", null=True, blank=True)  
    genre = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female")])
    age_range = models.CharField(max_length=10, choices=[
        ("05-15", "05-15 ans"), ("16-25", "16-25 ans"), 
        ("26-35", "26-35 ans"), ("36-45", "36-45 ans"), ("46+", "46 ans et plus")
    ])
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    imc = models.FloatField(null=True, blank=True)  
    diabetes_type = models.CharField(choices=[
        ('Type 1', 'Type 1'), ('Type 2', 'Type 2'), 
        ('Gestational', 'Gestational'), ('Pre-diabetes', 'Pre-diabetes')
    ], max_length=20)

    # Tests de glycémie
    fasting_glucose = models.FloatField(null=True, blank=True)  
    postprandial_glucose = models.FloatField(null=True, blank=True)

    # Conditions médicales supplémentaires
    hypertension = models.BooleanField(default=False)
    dyslipidemia = models.BooleanField(default=False)
    kidney_disease = models.BooleanField(default=False)
    obesity = models.BooleanField(default=False)

    # Complications possibles
    complications = models.JSONField(default=dict)

    completed = models.BooleanField(default=False)  # False = temporaire, True = inscrit

    def calculate_imc(self):
        if self.weight and self.height:
            try:
                self.weight = float(self.weight)  # Convertit en float pour éviter les erreurs
                self.height = float(self.height)
                self.imc = round(self.weight / ((self.height / 100) ** 2), 1)
            except ValueError:
                self.imc = None  # Évite l'erreur si la conversion échoue

    def save(self, *args, **kwargs):
        self.calculate_imc()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient {self.user.email if self.user else 'Non inscrit'}"


class TemporaryPatient(models.Model):
    """Modèle utilisé pour stocker les données avant inscription. Une fois inscrit, les données sont migrées vers Patient."""
    genre = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female")])
    age_range = models.CharField(max_length=10, choices=[("05-15", "05-15 ans"), ("16-25", "16-25 ans"), ("26-35", "26-35 ans"), ("36-45", "36-45 ans"), ("46+", "46 ans et plus")])
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    diabetes_type = models.CharField(choices=[
        ('Type 1', 'Type 1'), ('Type 2', 'Type 2'), 
        ('Gestational', 'Gestational'), ('Pre-diabetes', 'Pre-diabetes')
    ], max_length=20)
    fasting_glucose = models.FloatField(null=True, blank=True)
    postprandial_glucose = models.FloatField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def migrate_to_patient(self, user):
        """Créer un profil `Patient` à partir de ce profil temporaire."""
        patient = Patient.objects.create(
            user=user,
            genre=self.genre,
            age_range=self.age_range,
            weight=self.weight,
            height=self.height,
            diabetes_type=self.diabetes_type,
            fasting_glucose=self.fasting_glucose,
            postprandial_glucose=self.postprandial_glucose,
            completed=True
        )
        self.delete()  # Supprimer les données temporaires
        return patient