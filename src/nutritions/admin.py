from django.contrib import admin
from .models import HabitudesAlimentaires, PlanRepas, TemporaryHabitudesAlimentaires, Article, Commentaire, Aliment, AlimentPlan

# Register your models here.
admin.site.register(HabitudesAlimentaires)
admin.site.register(TemporaryHabitudesAlimentaires)
admin.site.register(AlimentPlan)
admin.site.register(Aliment)
admin.site.register(PlanRepas)
admin.site.register(Article)
admin.site.register(Commentaire)