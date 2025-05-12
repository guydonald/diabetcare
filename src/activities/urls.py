from django.urls import path
from .views import activity_form_view, finalize_registration_activity, activity_step_one

urlpatterns = [
    path('activity/', activity_form_view, name='activity_form'),
    path("finalize_registration/", finalize_registration_activity, name="finalize_registration_activity"),
    path("form/step-one/", activity_step_one, name="activity_step_one"),
]