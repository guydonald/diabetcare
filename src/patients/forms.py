from django import forms
from .models import TemporaryPatient, Patient
from users.models import CustomUser

class TemporaryPatientForm(forms.ModelForm):
    class Meta:
        model = TemporaryPatient
        fields = ['genre', 'age_range', 'weight', 'height', 'diabetes_type', 'fasting_glucose', 'postprandial_glucose']
        
        widgets = {
            'genre': forms.RadioSelect(choices=[("male", "Homme"), ("female", "Femme")]),
            'age_range': forms.RadioSelect(choices=[
                ("05-15", "05-15 ans"), ("16-25", "16-25 ans"), 
                ("26-35", "26-35 ans"), ("36-45", "36-45 ans"), ("46+", "46 ans et plus")
            ]),
            'weight': forms.NumberInput(attrs={'class': 'input input-bordered', 'placeholder': 'Votre poids (kg)'}),
            'height': forms.NumberInput(attrs={'class': 'input input-bordered', 'placeholder': 'Votre taille (cm)'}),
            'diabetes_type': forms.Select(attrs={'class': 'select select-bordered'}),
            'fasting_glucose': forms.NumberInput(attrs={'class': 'input input-bordered', 'placeholder': 'Glycémie à jeun'}),
            'postprandial_glucose': forms.NumberInput(attrs={'class': 'input input-bordered', 'placeholder': 'Glycémie après repas'}),
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "genre", "age_range", "weight", "height", "diabetes_type",
            "fasting_glucose", "postprandial_glucose", "hypertension",
            "dyslipidemia", "kidney_disease", "obesity",
        ]
        widgets = {
            "genre": forms.Select(attrs={"class": "form-select"}),
            "age_range": forms.Select(attrs={"class": "form-select"}),
            "weight": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Poids en kg"}),
            "height": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Taille en cm"}),
            "diabetes_type": forms.Select(attrs={"class": "form-select"}),
            "fasting_glucose": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Glycémie à jeun"}),
            "postprandial_glucose": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Glycémie après repas"}),
            "hypertension": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "dyslipidemia": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "kidney_disease": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "obesity": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }