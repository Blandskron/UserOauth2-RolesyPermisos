from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Aseguramos que el email sea único
    username = models.CharField(max_length=30, blank=True)  # Puedes dejar el campo username opcional
    
    USERNAME_FIELD = 'email' 
    # Los campos de grupos y permisos siguen siendo los mismos
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

    REQUIRED_FIELDS = ['username']