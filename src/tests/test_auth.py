import pytest
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.mark.django_db
def test_authentication_security(client):
    # Données test : injection SQL et XSS
    test_data = [
        {"username": "donald' --", "password": "k&guy1998"},
        {"username": "<script>alert('XSS');</script>", "password": "password"},
        {"username": "test_user", "password": "' OR '1'='1"},
    ]

    for data in test_data:
        response = client.post(reverse('account_login'), data)
        assert response.status_code != 200, f"Test échoué pour {data['username']}"

    print("Les tests ont été réalisés avec succès !")
