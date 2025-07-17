from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from typing import Any


class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="topics/%Y/%m/%d", blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news:topic-detail", kwargs={"pk": self.pk})

    @property
    def active_newspapers_count(self):
        return self.newspapers.filter(is_published=True).count()


class Newspaper(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low Priority"),
        ("medium", "Medium Priority"),
        ("high", "High Priority"),
        ("urgent", "Urgent"),
    ]

    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    excerpt = models.TextField(
        max_length=300, blank=True, help_text="Short description for preview"
    )
    featured_image = models.ImageField(upload_to="newspapers/%Y/%m/%d", blank=True)
    published_date = models.DateField()
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    views_count = models.PositiveIntegerField(default=0)

    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="newspapers"
    )
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="newspapers", blank=True
    )
    tags = models.ManyToManyField("Tag", blank=True, related_name="newspapers")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Newspaper"
        verbose_name_plural = "Newspapers"
        ordering = ["-published_date", "-created"]
        indexes = [
            models.Index(fields=["published_date"]),
            models.Index(fields=["is_published"]),
            models.Index(fields=["priority"]),
        ]

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.full_name = None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Newspaper.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        if not self.excerpt:
            self.excerpt = (
                self.content[:297] + "..." if len(self.content) > 300 else self.content
            )
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news:newspaper-detail", kwargs={"pk": self.pk})

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=["views_count"])

    @property
    def publishers_list(self):
        return ", ".join([publisher.full_name for publisher in self.publishers.all()])

    @property
    def is_recent(self):
        return (timezone.now().date() - self.published_date).days <= 7

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0

    @property
    def approved_comments_count(self):
        return self.comments.filter(is_approved=True).count()


# Дод моделі для ширшого функціоналу 🔻
class Tag(models.Model):  # 🔻Теги для кращого розділення на категорії
    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=50, unique=True)
    color = models.CharField(
        max_length=7, default="#6c757d", help_text="Hex color code for tag display"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Comment(models.Model):  # Коментарі до новин 🔻
    newspaper = models.ForeignKey(
        Newspaper, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.newspaper.title}"


class NewspaperRating(models.Model):  # 🔻Рейтинг новин
    RATING_CHOICES = [
        (1, "Poor"),
        (2, "Fair"),
        (3, "Good"),
        (4, "Very Good"),
        (5, "Excellent"),
    ]

    newspaper = models.ForeignKey(
        Newspaper, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["newspaper", "user"]

    def __str__(self):
        return f"{self.user.username} rated {self.newspaper.title}: {self.rating}/5"


from django.db import models
from django.conf import settings


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    head = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_department",
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
