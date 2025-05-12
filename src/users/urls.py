from django.urls import path, include
from .views import (home, set_language, user_registration, dashboard, user_summary,
                    manage_patients, patient_details)

urlpatterns = [
    path("register/", user_registration, name="user_registration"),
    path('dashboard/', dashboard, name='dashboard'),
    path('accounts/', include('allauth.urls')),
    path('', home, name='accueil'),
    path("set_language/", set_language, name="set_language"),
    path("summary/", user_summary, name="user_summary"),
    path("users/manage-patients/", manage_patients, name="manage_patients"),
    path("users/patient/<int:patient_id>/", patient_details, name="patient_details"),
]
