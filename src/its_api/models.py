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

    author = models.ForeignKey(
        verbose_name='Auteur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Projet'

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(
        verbose_name='Utilisateur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )

    project = models.ForeignKey(
        verbose_name='Projet',
        to=Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    role = models.CharField(
            verbose_name='Rôle',
            max_length=50,
    )

    class Meta:
        verbose_name = 'Collaborateur'
        unique_together = ('user', 'project')


class Issue(models.Model):
    title = models.CharField(
        verbose_name='Titre',
        max_length=128,
        blank=False
    )

    description = models.CharField(
        verbose_name='Description',
        max_length=512
    )

    tag = models.CharField(
        verbose_name='Type',
        max_length=64
    )

    priority = models.CharField(
        verbose_name='Priorité',
        max_length=64
    )

    status = models.CharField(
        verbose_name='Statut',
        max_length=64
    )

    project = models.ForeignKey(
        verbose_name='Projet',
        to=Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        verbose_name='Date',
        auto_now_add=True
    )

    author = models.ForeignKey(
        verbose_name='Auteur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='Auteur',
        blank=True,
        null=True
    )

    assignee = models.ForeignKey(
        verbose_name='Assigné',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='Assigné',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Problème'


class Comment(models.Model):
    description = models.CharField(
        verbose_name='Description',
        max_length=2056
    )

    author = models.ForeignKey(
        verbose_name='Auteur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    issue = models.ForeignKey(
        verbose_name='Problème',
        to=Issue,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        verbose_name='Date',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Commentaire'
