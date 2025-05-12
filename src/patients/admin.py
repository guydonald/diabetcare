from django.contrib import admin
from .models import Patient, TemporaryPatient

# Register your models here.

admin.site.register(Patient)
admin.site.register(TemporaryPatient)