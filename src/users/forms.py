from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from allauth.account.forms import SignupForm
from patients.models import Patient
# Tes fonctions de migration
from nutritions.views import finalize_registration_nutrition
from activities.views import finalize_registration_activity
from patients.views import finalize_registration_patient


class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription basé sur CustomUser"""
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "input", "placeholder": "Email"}))
    
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(attrs={"class": "input", "placeholder": "Nom d'utilisateur"}),
            "password1": forms.PasswordInput(attrs={"class": "input", "placeholder": "Mot de passe"}),
            "password2": forms.PasswordInput(attrs={"class": "input", "placeholder": "Confirmer le mot de passe"}),
        }


class MyCustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="first name")
    last_name = forms.CharField(max_length=30, label="last name")

    widgets = {
        "first_name": forms.TextInput(attrs={"class": "input", "placeholder": "Nom d'utilisateur"}),
        "last_name": forms.TextInput(attrs={"class": "input", "placeholder": "Mot de passe"}),
    }
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # Pré-remplir depuis la session
        if self.request:
            activity_data = self.request.session.get('activity_data')
            if activity_data:
                # Tu peux aussi mettre d'autres pré-remplissages ici
                self.fields['last_name'].initial = activity_data.get('last_name', '')
                self.fields['first_name'].initial = activity_data.get('first_name', '')
                self.fields['username'].initial = activity_data.get('username', '')

    def save(self, request):
        user = super().save(request)

        try:
            finalize_registration_patient(request, user)
            finalize_registration_nutrition(request, user)
            finalize_registration_activity(request, user)
        except Patient.DoesNotExist:
            # ✅ On ignore l'erreur et on continue l'inscription normalement
            pass
        except Exception as e:
            # 🔥 Logger l'erreur pour surveiller les éventuels problèmes
            print(f"Erreur lors de la finalisation de l'inscription : {e}")
        return user
