from django.conf import settings
from django.db import models


class Project(models.Model):
    title = models.CharField(
        verbose_name='Titre',
        max_length=128,
        blank=False
    )

    description = models.CharField(
        verbose_name='Description',
        max_length=512
    )

    type = models.CharField(
        verbose_name='Type',
        max_length=64
    )

    author_user_id = models.ForeignKey(
        verbose_name='Auteur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Projet'

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user_id = models.ForeignKey(
        verbose_name='Utilisateur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    project_id = models.ForeignKey(
        verbose_name='Projet',
        to=Project,
        on_delete=models.CASCADE
    )

    role = models.CharField(
            verbose_name='Rôle',
            max_length=50,
    )

    class Meta:
        verbose_name = 'Collaborateur'
