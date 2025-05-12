from django.db import models
from users.models import CustomUser
from patients.models import Patient

# Create your models here.
class HabitudesAlimentaires(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="habitudes_alimentaires")
    habitudes = models.JSONField(default=dict, verbose_name="Habitudes alimentaires")  # Stocke plusieurs choix
    frequence_repas = models.CharField(
        max_length=20, choices=[
            ("1x", "One time"), ("2x", "Two times"), 
            ("3x", "Three times"), ("4x+", "Four times or more")
        ],
        verbose_name="Fréquence des repas"
    )
    portion = models.CharField(
        max_length=10, choices=[("petite", "Little"), ("modérée", "Moderate"), ("grande", "Large")], 
        verbose_name="Taille de portion"
    )
    methode_cuisson = models.JSONField(default=dict, verbose_name="Méthodes de cuisson")  # Permet plusieurs choix
    eau_consommee = models.CharField(
        max_length=20, choices=[
            ("-0.5L", "Less than 0.5L"), ("0.5-1.5L", "0.5 - 1.5L"), 
            ("1.5-2.5L", "1.5 - 2.5L"), ("2.5L+", "More than 2.5L")
        ],
        verbose_name="Quantité d’eau consommée"
    )

    def __str__(self):
        return f"Habitudes alimentaires de {self.patient.user.email}"
    

CHOIX_HABITUDES = [
    ("eat_late", "Manger tard le soir"),
    ("love_sweets", "Aime les sucreries"),
    ("skip_breakfast", "Saute le petit déjeuner"),
    ("high_fat_foods", "Consomme beaucoup de matières grasses"),
]

CHOIX_CUISSON = [
    ("fried", "Frit"),
    ("grilled", "Grillé"),
    ("boiled", "Bouilli"),
    ("steamed", "À la vapeur"),
]

CHOIX_DIET = [
    ("vegetarian", "Végétarien"),
    ("vegan", "Végan"),
    ("gluten_free", "Sans gluten"),
    ("low_carb", "Faible en glucides"),
]

CHOIX_PRODUITS = [
    ("vegetables", "Légumes"),
    ("cereals", "Céréales et pains"),
    ("meat", "Viandes et œufs"),
    ("fish", "Poisson"),
    ("dairy", "Produits laitiers"),
    ("fruits", "Fruits et baies"),
    ("other", "Autres produits"),
]

class TemporaryHabitudesAlimentaires(models.Model):
    """Stocke temporairement les réponses du formulaire nutritionnel avant inscription"""
    session_id = models.CharField(max_length=255, verbose_name="ID de session")

    # Habitudes alimentaires
    eating_habits = models.JSONField(default=dict, verbose_name="Habitudes alimentaires")
    meal_frequency = models.CharField(
        max_length=20, choices=[
            ("1x", "Une fois"), ("2x", "Deux fois"), 
            ("3x", "Trois fois"), ("4x+", "Quatre fois ou plus")
        ],
        verbose_name="Fréquence des repas"
    )
    portion_size = models.CharField(
        max_length=10, choices=[
            ("petite", "Petite"), ("modérée", "Modérée"), ("grande", "Grande")
        ],
        verbose_name="Taille de portion"
    )
    cooking_methods = models.JSONField(default=dict, verbose_name="Méthodes de cuisson")
    water_intake = models.CharField(
        max_length=50, choices=[
            ('less_0.5L', 'Moins de 0.5L'), 
            ('0.5-1.5L', '0.5 - 1.5L'), 
            ('1.5-2.5L', '1.5 - 2.5L'), 
            ('more_2.5L', 'Plus de 2.5L')
        ],
        verbose_name="Consommation d'eau"
    )
    diet_preferences = models.JSONField(default=dict, verbose_name="Régime alimentaire")
    favorite_products = models.JSONField(default=dict, verbose_name="Produits favoris")

    def __str__(self):
        return f"Données nutrition temporaires - Session {self.session_id}"   


class Aliment(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de l’aliment")
    categorie = models.CharField(
        max_length=50, choices=[
            ("vegetables", "Légumes"), ("cereals", "Céréales et Pains"), ("meat", "Viande et Œufs"),
            ("fish", "Poisson"), ("dairy", "Produits laitiers"), ("fruits", "Fruits et Baies"),
            ("other", "Autres produits")
        ],
        verbose_name="Catégorie"
    )
    calories = models.FloatField(verbose_name="Calories")
    proteines = models.FloatField(verbose_name="Protéines")
    lipides = models.FloatField(verbose_name="Lipides")
    glucides = models.FloatField(verbose_name="Glucides")

    def __str__(self):
        return f"{self.nom} ({self.categorie})"
    

class PlanRepas(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="plans_repas")
    nom_plan = models.CharField(max_length=100, verbose_name="Nom du plan de repas")
    description = models.TextField(null=True, blank=True, verbose_name="Description du plan")
    date_creation = models.DateField(auto_now_add=True, verbose_name="Date de création")
    date_updated = models.DateField(auto_now=True, verbose_name="Dernière modification")
    aliments = models.ManyToManyField(Aliment, through="AlimentPlan", verbose_name="Aliments inclus")

    def __str__(self):
        return self.nom_plan
    

class AlimentPlan(models.Model):
    plan_repas = models.ForeignKey(PlanRepas, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    quantite = models.FloatField()  # Exemple : 100g


class Article(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    contenu = models.TextField(verbose_name="Contenu de l’article")
    date_publication = models.DateField(auto_now_add=True, verbose_name="Date de publication")
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Auteur")

    class Meta:
        ordering = ["-date_publication"]  # Affiche les articles du plus récent au plus ancien

    def __str__(self):
        return self.titre
    

class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Article concerné")
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Utilisateur")
    contenu = models.TextField(verbose_name="Commentaire")
    date_commentaire = models.DateField(auto_now_add=True, verbose_name="Date du commentaire")

    class Meta:
        ordering = ["-date_commentaire"]

    def __str__(self):
        return f"Commentaire de {self.utilisateur.email} sur {self.article.titre}"