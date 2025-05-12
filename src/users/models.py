import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Modèle utilisateur personnalisé avec UUID et authentification par email"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_patient = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    last_login = models.DateTimeField(auto_now=True, null=True, verbose_name="Dernière connexion")

    USERNAME_FIELD = 'email'  # Authentification basée sur l'email
    REQUIRED_FIELDS = ['username']  # Le champ "username" reste obligatoire pour Django

    def __str__(self):
        return self.email