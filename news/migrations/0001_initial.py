# Generated by Django 5.2.4 on 2025-07-16 08:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=50, unique=True)),
                ("slug", models.SlugField(unique=True)),
                (
                    "color",
                    models.CharField(
                        default="#6c757d",
                        help_text="Hex color code for tag display",
                        max_length=7,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=100, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, upload_to="topics/%Y/%m/%d")),
                ("is_active", models.BooleanField(default=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Topic",
                "verbose_name_plural": "Topics",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "head",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="headed_department",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Newspaper",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(db_index=True, max_length=200)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("content", models.TextField()),
                (
                    "excerpt",
                    models.TextField(
                        blank=True,
                        help_text="Short description for preview",
                        max_length=300,
                    ),
                ),
                (
                    "featured_image",
                    models.ImageField(blank=True, upload_to="newspapers/%Y/%m/%d"),
                ),
                ("published_date", models.DateField()),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("low", "Low Priority"),
                            ("medium", "Medium Priority"),
                            ("high", "High Priority"),
                            ("urgent", "Urgent"),
                        ],
                        default="medium",
                        max_length=10,
                    ),
                ),
                ("is_published", models.BooleanField(default=True)),
                (
                    "is_featured",
                    models.BooleanField(default=False, help_text="Show on homepage"),
                ),
                ("views_count", models.PositiveIntegerField(default=0)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "publishers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="newspapers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True, related_name="newspapers", to="news.tag"
                    ),
                ),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="newspapers",
                        to="news.topic",
                    ),
                ),
            ],
            options={
                "verbose_name": "Newspaper",
                "verbose_name_plural": "Newspapers",
                "ordering": ["-published_date", "-created"],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(max_length=500)),
                ("is_approved", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "newspaper",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="news.newspaper",
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="NewspaperRating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Poor"),
                            (2, "Fair"),
                            (3, "Good"),
                            (4, "Very Good"),
                            (5, "Excellent"),
                        ]
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "newspaper",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="news.newspaper",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("newspaper", "user")},
            },
        ),
        migrations.AddIndex(
            model_name="newspaper",
            index=models.Index(
                fields=["published_date"], name="news_newspa_publish_7b17e4_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="newspaper",
            index=models.Index(
                fields=["is_published"], name="news_newspa_is_publ_a87a3f_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="newspaper",
            index=models.Index(
                fields=["priority"], name="news_newspa_priorit_b868bd_idx"
            ),
        ),
    ]
