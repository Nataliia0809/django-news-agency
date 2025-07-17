from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date
from .models import Topic, Newspaper, Tag, Department
from .forms import NewspaperForm, TopicForm, SearchForm

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            name="Test Topic", description="Test description"
        )
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_topic_str(self):
        self.assertEqual(str(self.topic), "Test Topic")

    def test_topic_slug_generation(self):
        self.assertEqual(self.topic.slug, "test-topic")

    def test_newspaper_creation(self):
        newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Test content for newspaper",
            published_date=date.today(),
            topic=self.topic,
        )
        self.assertEqual(newspaper.slug, "test-newspaper")
        self.assertTrue(newspaper.excerpt)  # Auto-generated excerpt

    def test_newspaper_get_absolute_url(self):
        newspaper = Newspaper.objects.create(
            title="Test News",
            content="Test content",
            published_date=date.today(),
            topic=self.topic,
        )
        expected_url = reverse("news:newspaper-detail", kwargs={"pk": newspaper.pk})
        self.assertEqual(newspaper.get_absolute_url(), expected_url)

    def test_redactor_full_name_property(self):
        user = User.objects.create_user(
            username="john",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
        )
        self.assertEqual(user.full_name, "John Doe")


class FormTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic")
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_newspaper_form_valid_data(self):
        form_data = {
            "title": "Test Newspaper",
            "content": "Test content for the newspaper",
            "published_date": date.today(),
            "topic": self.topic.id,
            "publishers": [self.user.id],
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_newspaper_form_missing_required_fields(self):
        form_data = {"title": "", "content": "Test content"}
        form = NewspaperForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_topic_form_valid_data(self):
        form_data = {"name": "New Topic"}
        form = TopicForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_optional_fields(self):
        form_data = {
            "query": "test search",
            "topic": self.topic.id,
            "author": self.user.id,
        }
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.topic = Topic.objects.create(name="Test Topic")
        self.newspaper = Newspaper.objects.create(
            title="Test News",
            content="Test content",
            published_date=date.today(),
            topic=self.topic,
        )

    def test_index_view(self):
        response = self.client.get(reverse("news:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test News")

    def test_newspaper_list_view(self):
        response = self.client.get(reverse("news:newspaper-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test News")

    def test_newspaper_detail_view(self):
        response = self.client.get(
            reverse("news:newspaper-detail", kwargs={"pk": self.newspaper.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.newspaper.title)

    def test_newspaper_create_requires_login(self):
        response = self.client.get(reverse("news:newspaper-create"))
        self.assertRedirects(response, "/accounts/login/?next=/newspapers/create/")

    def test_newspaper_create_with_login(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("news:newspaper-create"))
        self.assertEqual(response.status_code, 200)

    def test_topic_list_view(self):
        response = self.client.get(reverse("news:topic-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Topic")

    def test_search_view(self):
        response = self.client.get(reverse("news:search"), {"query": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test News")

    def test_search_autocomplete(self):
        response = self.client.get(reverse("news:search-autocomplete"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")


class URLTests(TestCase):
    def test_url_patterns(self):
        urls = [
            ("news:index", {}),
            ("news:newspaper-list", {}),
            ("news:topic-list", {}),
            ("news:redactor-list", {}),
            ("news:search", {}),
        ]

        for url_name, kwargs in urls:
            with self.subTest(url_name=url_name):
                url = reverse(url_name, kwargs=kwargs)
                self.assertTrue(url.startswith("/"))


class AdminTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass123"
        )
        self.client.login(username="admin", password="adminpass123")

    def test_admin_access(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

    def test_newspaper_admin_list(self):
        response = self.client.get("/admin/news/newspaper/")
        self.assertEqual(response.status_code, 200)

    def test_topic_admin_list(self):
        response = self.client.get("/admin/news/topic/")
        self.assertEqual(response.status_code, 200)
