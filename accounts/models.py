from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(
        help_text="Years of experience in journalism"
    )
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', blank=True)
    phone = models.CharField(max_length=15, blank=True)
    department = models.ForeignKey('news.Department', on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='redactors')
    is_active_redactor = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='redactor_groups',
        blank=True,
        help_text='The groups this redactor belongs to.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='redactor_permissions',
        blank=True,
        help_text='Specific permissions for this redactor.',
    )

    class Meta:
        verbose_name = "Redactor"
        verbose_name_plural = "Redactors"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def published_newspapers_count(self):
        return self.newspapers.filter(is_published=True).count()

    @property
    def total_views(self):
        return sum(newspaper.views_count for newspaper in self.newspapers.all())