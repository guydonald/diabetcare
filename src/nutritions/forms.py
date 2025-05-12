from django import forms
from .models import TemporaryHabitudesAlimentaires, HabitudesAlimentaires,CHOIX_HABITUDES, CHOIX_CUISSON, CHOIX_DIET, CHOIX_PRODUITS, Article, Commentaire

class TemporaryHabitudesAlimentairesForm(forms.ModelForm):
    eating_habits = forms.MultipleChoiceField(
        choices=CHOIX_HABITUDES, widget=forms.CheckboxSelectMultiple, required=False
    )
    cooking_methods = forms.MultipleChoiceField(
        choices=CHOIX_CUISSON, widget=forms.CheckboxSelectMultiple, required=False
    )
    diet_preferences = forms.MultipleChoiceField(
        choices=CHOIX_DIET, widget=forms.CheckboxSelectMultiple, required=False
    )
    favorite_products = forms.MultipleChoiceField(
        choices=CHOIX_PRODUITS, widget=forms.CheckboxSelectMultiple, required=False
    )


    class Meta:
        model = TemporaryHabitudesAlimentaires
        fields = ['eating_habits', 'meal_frequency', 'portion_size', 'cooking_methods', 'water_intake', 'diet_preferences', 'favorite_products']

        widgets = {
            'meal_frequency': forms.RadioSelect(),
            'portion_size': forms.RadioSelect(),
            'water_intake': forms.RadioSelect(),
        }

class HabitudesAlimentairesForm(forms.ModelForm):
    class Meta:
        model = HabitudesAlimentaires
        fields = [
            "frequence_repas", "portion", "eau_consommee", "habitudes", "methode_cuisson"
        ]
        widgets = {
            "frequence_repas": forms.Select(attrs={"class": "form-select"}),
            "portion": forms.Select(attrs={"class": "form-select"}),
            "eau_consommee": forms.Select(attrs={"class": "form-select"}),
            "habitudes": forms.CheckboxSelectMultiple(choices=CHOIX_HABITUDES),
            "methode_cuisson": forms.CheckboxSelectMultiple(choices=CHOIX_CUISSON),
        }
    def clean_habitudes(self):
        # Transformer en dictionnaire avant de sauvegarder
        return {habit: True for habit in self.cleaned_data['habitudes']}

    def clean_methode_cuisson(self):
        return {method: True for method in self.cleaned_data['methode_cuisson']}
    
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["titre", "contenu"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Titre de l'article"}),
            "contenu": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Contenu de l'article"}),
        }

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ["contenu"]
        widgets = {
            "contenu": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Écrivez votre commentaire ici..."}),
        }
