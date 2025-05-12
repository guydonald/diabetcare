from django.urls import path
from .views import nutrition_form_view, finalize_registration_nutrition, habitudes_step_one, list_articles, article_detail, create_article, articles_view


urlpatterns = [
    path('step-nutrition', nutrition_form_view, name='nutrition-form'),
    path("finalize_registration/", finalize_registration_nutrition, name="finalize_registration_nutrition"),
    path("form/step-one/", habitudes_step_one, name="habitudes_step_one"),
    path("article/", list_articles, name="list_articl"),
    path("articles/<int:article_id>/", article_detail, name="article_detail"),
    path("articles/new/", create_article, name="create_article"),
    path("articles/", articles_view, name="list_articles"),
]
