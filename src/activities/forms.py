from django import forms
from .models import TemporaryActivityProfile, ActivityProfile, CHOIX_ACTIVITÉ

class TemporaryActivityProfileForm(forms.ModelForm):
    activity_type = forms.MultipleChoiceField(
        choices=[
            ("none", "Je ne fais pas de sport"),
            ("walking", "Marche"),
            ("running", "Course à pied"),
            ("cycling", "Cyclisme"),
            ("swimming", "Natation"),
            ("gym", "Salle de sport"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    physical_activity_frequency = forms.ChoiceField(
        choices=[
            ("none", "Jamais"),
            ("once", "Une fois par semaine"),
            ("twice", "Deux fois par semaine"),
            ("thrice", "Trois fois par semaine"),
            ("more_than_thrice", "Plus de trois fois"),
        ],
        widget=forms.RadioSelect
    )

    intensity_level = forms.ChoiceField(
        choices=[
            ("none", "Non applicable"),
            ("low", "Faible"),
            ("moderate", "Modéré"),
            ("high", "Élevé"),
        ],
        widget=forms.RadioSelect
    )
    class Meta:
        model = TemporaryActivityProfile
        fields = ['activity_type', 'physical_activity_duration', 'physical_activity_frequency', 'intensity_level', 'sleep_hours', 'stress_level']

class ActivityProfileForm(forms.ModelForm):
    class Meta:
        model = ActivityProfile
        fields = [
            "activity_type", "physical_activity_duration", "physical_activity_frequency",
            "intensity_level", "sleep_hours", "stress_level"
        ]
        widgets = {
            "activity_type": forms.CheckboxSelectMultiple(choices=CHOIX_ACTIVITÉ),
            "physical_activity_duration": forms.Select(attrs={"class": "form-select"}),
            "physical_activity_frequency": forms.Select(attrs={"class": "form-select"}),
            "intensity_level": forms.Select(attrs={"class": "form-select"}),
            "sleep_hours": forms.Select(attrs={"class": "form-select"}),
            "stress_level": forms.Select(attrs={"class": "form-select"}),
        }
    def clean_activity_type(self):
        return {activity: True for activity in self.cleaned_data['activity_type']}
