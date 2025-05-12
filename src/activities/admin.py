from django.contrib import admin
from .models import TemporaryActivityProfile, ActivityProfile

# Register your models here.

admin.site.register(TemporaryActivityProfile)
admin.site.register(ActivityProfile)