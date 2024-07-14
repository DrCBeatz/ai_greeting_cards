# accounts/tests/test_accounts.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_create_user():
    User = get_user_model()
    user = User.objects.create_user(
        username="test", email="test@email.com", password="testpass123"
    )
    assert user.username == "test"
    assert user.email == "test@email.com"
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_superuser():
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        username="superadmin", email="superadmin@email.com", password="testpass123"
    )
    assert admin_user.username == "superadmin"
    assert admin_user.email == "superadmin@email.com"
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser

@pytest.mark.django_db
def test_signup_template(client):
    url = reverse("signup")
    response = client.get(url)

    assert response.status_code == 200
    assert "signup.html" in [t.name for t in response.templates]
    assert "Sign Up" in response.content.decode("utf-8")
    assert "Hi there! I should not be on the page." not in response.content.decode()
