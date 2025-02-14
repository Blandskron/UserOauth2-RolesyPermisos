from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.conf import settings

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    id_user = models.BigAutoField(primary_key=True)
    username = None
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    identification = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'tbl_users'
        managed = True


# Modelo de Documentos con control de permisos
class Document(models.Model):
    title = models.CharField(max_length=255)
    hash_name = models.CharField(unique=True, max_length=255)
    path = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    size_bytes = models.BigIntegerField()
    status = models.BooleanField(default=True)
    metadata = models.JSONField(blank=True, null=True)
    local_create_time = models.DateTimeField()
    local_update_time = models.DateTimeField(blank=True, null=True)
    server_create_time = models.DateTimeField()
    server_update_time = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group, blank=True)  # Control de acceso por grupos

    class Meta:
        db_table = 'tbl_documents'
        managed = True

    def __str__(self):
        return self.title

# Modelo de Logs
class Log(models.Model):
    action = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(blank=True, null=True)
    entity = models.CharField(max_length=255, blank=True, null=True)
    entity_id = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'tbl_logs'
        managed = True 
