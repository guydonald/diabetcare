from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.html import escape
from django.contrib import messages
from .forms import TemporaryHabitudesAlimentairesForm, HabitudesAlimentairesForm, ArticleForm, CommentaireForm
from .models import HabitudesAlimentaires, Article, Commentaire
from patients.models import Patient

# Create your views here.

def nutrition_form_view(request):
    """Afficher le formulaire de nutrition et enregistrer temporairement les données en session"""
    if request.method == 'POST':
        form = TemporaryHabitudesAlimentairesForm(request.POST)
        if form.is_valid():
            nutrition_data = form.cleaned_data
            
            # Stocker les réponses en session Django
            request.session['nutrition_data'] = nutrition_data

            return redirect('activity_form')  # Rediriger vers l’étape suivante (activité physique)
    else:
        form = TemporaryHabitudesAlimentairesForm()
    
    return render(request, 'nutritions/nutrition_form.html', {'form': form})

def finalize_registration_nutrition(request, user):
    """Migration des habitudes alimentaires après inscription"""
    patient = Patient.objects.get(user=user)
    temp_nutrition = request.session.get("nutrition_data")
    print("Données nutrition récupérées :", temp_nutrition)
    
    if temp_nutrition:
        HabitudesAlimentaires.objects.create(
            patient=patient,
            habitudes=temp_nutrition["eating_habits"],
            frequence_repas=temp_nutrition["meal_frequency"],
            portion=temp_nutrition["portion_size"],
            methode_cuisson=temp_nutrition["cooking_methods"],
            eau_consommee=temp_nutrition["water_intake"]
        )
        del request.session["nutrition_data"]

    return patient

@login_required
def habitudes_step_one(request):
    patient = get_object_or_404(Patient, user=request.user)
    habitudes = patient.habitudes_alimentaires.first()  # On suppose qu'il n'a qu'un seul set d'habitudes

    form = HabitudesAlimentairesForm(instance=habitudes)
    if request.method == "POST":
        form = HabitudesAlimentairesForm(request.POST, instance=habitudes)
        if form.is_valid():
            new_habitudes = form.save(commit=False)
            
            # Escape les champs texte si besoin
            new_habitudes.frequence_repas = escape(new_habitudes.frequence_repas)
            new_habitudes.portion = escape(new_habitudes.portion)
            new_habitudes.eau_consommee = escape(new_habitudes.eau_consommee)
            
            new_habitudes.patient = patient
            new_habitudes.save()
            messages.success(request, "Vos habitudes alimentaires ont été mises à jour avec succès !")
            return redirect("activity_step_one")
    return render(request, "nutritions/habitudes_step_one.html", {"form": form})

def is_admin(user):
    return user.is_admin  # Vérifie si l'utilisateur est un administrateur

@login_required
def list_articles(request):
    """Affiche la liste des articles avec pagination."""
    articles = Article.objects.all()
    return render(request, "nutritions/list_articl.html", {"articles": articles})

@login_required
def article_detail(request, article_id):
    """Affiche les détails d’un article avec ses commentaires."""
    article = get_object_or_404(Article, id=article_id)
    commentaires = Commentaire.objects.filter(article=article)

    if request.method == "POST":
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = article
            commentaire.utilisateur = request.user
            commentaire.save()
            messages.success(request, "Votre commentaire a été ajouté avec succès !")
            return redirect("article_detail", article_id=article.id)
    else:
        form = CommentaireForm()

    return render(request, "nutritions/article_detail.html", {
        "article": article,
        "commentaires": commentaires,
        "form": form
    })

@login_required
def articles_view(request):
    """Affiche la liste des articles avec commentaires et permet l’ajout d’un nouvel article (admin uniquement)."""
    articles = Article.objects.all()

    # Préparer le formulaire d'ajout d'article pour les administrateurs
    form_article = ArticleForm() if request.user.is_admin else None

    # Préparer les formulaires de commentaires pour chaque article
    form_commentaires = {article.id: CommentaireForm() for article in articles}

    if request.method == "POST":
        if request.user.is_admin and "create_article" in request.POST:
            form_article = ArticleForm(request.POST)
            if form_article.is_valid():
                article = form_article.save(commit=False)
                article.auteur = request.user
                article.save()
                messages.success(request, "Article publié avec succès !")
                return redirect("list_articles")

        elif "post_comment" in request.POST:
            article_id = request.POST.get("article_id")
            article = get_object_or_404(Article, id=article_id)
            form_commentaire = CommentaireForm(request.POST)
            if form_commentaire.is_valid():
                commentaire = form_commentaire.save(commit=False)
                commentaire.article = article
                commentaire.utilisateur = request.user
                commentaire.save()
                messages.success(request, "Votre commentaire a été ajouté avec succès !")
                return redirect("list_articles")

    return render(request, "nutritions/list_articles.html", {
        "articles": articles,
        "form_article": form_article,
        "form_commentaires": form_commentaires
    })

@login_required
@user_passes_test(is_admin)
def create_article(request):
    """Vue permettant aux administrateurs de publier un nouvel article."""
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.save()
            messages.success(request, "Article publié avec succès !")
            return redirect("list_articles")
    else:
        form = ArticleForm()

    return render(request, "nutritions/create_article.html", {"form": form})