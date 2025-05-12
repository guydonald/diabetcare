from django.urls import path
from .views import temporary_patient_form_view, finalize_registration_patient, patient_step_one, patient_step_two

urlpatterns = [
    path('patients', temporary_patient_form_view, name='patients'),
    path("finalize_registration/", finalize_registration_patient, name="finalize_registration_patient"),
    path("form/step-one/", patient_step_one, name="patient_step_one"),
    path("form/step-two/", patient_step_two, name="patient_step_two"),
]
