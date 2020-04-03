from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from datetime import datetime
import uuid


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_attributes):
        """Creates a saves a new user"""
        if not email:
            raise ValueError('User should have email address')
        user = self.model(
            email=self.normalize_email(email),
            **extra_attributes)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates a super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def delete(self):
        self.deleted_at = datetime.utcnow()
        self.is_deleted = True
        self.save()


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=10, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(BaseModel):
	"""Recipe Object"""
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
	)
	title = models.CharField(max_length=255)
	time_in_minutes = models.IntegerField()
	price = models.DecimalField(max_digits=5, decimal_places=2)
	link = models.CharField(max_length=255, blank=True)
	ingredients = models.ManyToManyField('Ingredient')
	tags = models.ManyToManyField('Tag')

	def __str__(self):
		return self.title


class Tag(BaseModel):
    """Tag to be used for recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingredient(BaseModel):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
