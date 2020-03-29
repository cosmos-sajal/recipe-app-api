from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""
        email = "test@gmail.com"
        password = "test_password_123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_normalized_email_successful(self):
        """Test creating a new user with normalized email is successful"""
        email = "test@GMAIL.COM"
        password = "test_password_123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        """Test if the user email is invalid"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password="123")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="test@gmail.com",
            password="test123"
        )

        self.assertTrue(user.is_superuser)
