from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Vous devez rentrer un email valide.")
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        superuser = self.create_user(
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.save()
        return superuser


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Utilisateur'

    email = models.EmailField(
        max_length=40,
        unique=True,
        blank=False
    )

    first_name = models.CharField(
        verbose_name='Prénom',
        max_length=50,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        verbose_name='Nom',
        max_length=50,
        blank=True,
        null=True
    )

    password = models.CharField(
        verbose_name='Mot de passe',
        max_length=128,
    )
    last_login = models.DateTimeField(
        verbose_name="Dernière connexion",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


