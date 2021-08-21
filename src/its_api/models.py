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

    project_id = models.ForeignKey(
        verbose_name='Projet',
        to=Project,
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(
        verbose_name='Date',
        auto_now_add=True
    )

    author_user_id = models.ForeignKey(
        verbose_name='Auteur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='Auteur'
    )

    assignee_user_id = models.ForeignKey(
        verbose_name='Assigné',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='Assigné',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Problème'

    def save(self, *args, **kwargs):
        if not self.assignee_user_id:
            self.assignee_user_id = self.author_user_id
        super().save(*args, **kwargs)


class Comment(models.Model):
    description = models.CharField(
        verbose_name='Description',
        max_length=2056
    )

    author_user_id = models.ForeignKey(
        verbose_name='Auteur',
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    issue_id = models.ForeignKey(
        verbose_name='Problème',
        to=Issue,
        on_delete=models.CASCADE
    )

    created = models.DateTimeField(
        verbose_name='Date',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Commentaire'
