from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Newspaper, Topic
from .forms import NewspaperForm, TopicForm, RedactorForm
from accounts.models import Redactor
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .forms import SearchForm
from django.urls import reverse
from django.http import JsonResponse


# Home page🔻
def index(request):
    newspapers = Newspaper.objects.all()[:5]
    context = {
        "newspapers": newspapers,
        "total_newspapers": Newspaper.objects.count(),
        "total_topics": Topic.objects.count(),
        "total_redactors": Redactor.objects.count(),
    }
    return render(request, "news/index.html", context)


# newspaper🔻
class NewspaperListView(ListView):
    model = Newspaper
    template_name = "news/newspaper_list.html"
    context_object_name = "newspapers"
    paginate_by = 10

    def get_queryset(self):
        queryset = Newspaper.objects.select_related("topic").prefetch_related(
            "publishers"
        )
        topic_id = self.request.GET.get("topic")
        if topic_id:
            queryset = queryset.filter(topic__id=topic_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        context["selected_topic"] = self.request.GET.get("topic")
        return context


class NewspaperDetailView(DetailView):
    model = Newspaper
    template_name = "news/newspaper_detail.html"


class NewspaperCreateView(LoginRequiredMixin, CreateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "news/newspaper_create.html"

    def form_valid(self, form):
        newspaper = form.save(commit=False)
        newspaper.save()
        publishers = form.cleaned_data.get("publishers")
        if publishers:
            newspaper.publishers.set(publishers)
        else:
            newspaper.publishers.add(self.request.user)

        return super().form_valid(form)


class NewspaperUpdateView(LoginRequiredMixin, UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "news/newspaper_update.html"


class NewspaperDeleteView(LoginRequiredMixin, DeleteView):
    model = Newspaper
    template_name = "news/newspaper_delete.html"
    success_url = reverse_lazy("news:newspaper-list")


# topics🔻
class TopicListView(ListView):
    model = Topic
    template_name = "news/topic_list.html"


class TopicDetailView(DetailView):
    model = Topic
    template_name = "news/topic_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["newspapers"] = self.object.newspaper_set.all()
        context["newspapers"] = self.object.newspapers.all()
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "news/topic_create.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Тема "{self.object.name}" успішно створена!')
        return response  # Повертаємо response

    def get_success_url(self):
        return reverse_lazy("news:topic-detail", kwargs={"pk": self.object.pk})


# redactors🔻
class RedactorListView(ListView):
    model = Redactor
    template_name = "news/redactor_list.html"
    context_object_name = "redactors"
    paginate_by = 10


class RedactorCreateView(LoginRequiredMixin, CreateView):
    model = Redactor
    form_class = RedactorForm
    template_name = "news/redactor_create.html"


class RedactorDetailView(DetailView):
    model = Redactor
    template_name = "news/redactor_detail.html"
    context_object_name = "redactor"


# search🔻
def search_view(request):
    form = SearchForm(request.GET or None)
    newspapers = Newspaper.objects.filter(is_published=True)
    query = None

    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            newspapers = newspapers.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(excerpt__icontains=query)
                | Q(topic__name__icontains=query)
                | Q(publishers__first_name__icontains=query)
                | Q(publishers__last_name__icontains=query)
                | Q(publishers__username__icontains=query)
            ).distinct()

        topic = form.cleaned_data.get("topic")
        if topic:
            newspapers = newspapers.filter(topic=topic)

        author = form.cleaned_data.get("author")
        if author:
            newspapers = newspapers.filter(publishers=author)

        date_from = form.cleaned_data.get("date_from")
        if date_from:
            newspapers = newspapers.filter(published_date__gte=date_from)

        date_to = form.cleaned_data.get("date_to")
        if date_to:
            newspapers = newspapers.filter(published_date__lte=date_to)

        priority = form.cleaned_data.get("priority")
        if priority:
            newspapers = newspapers.filter(priority=priority)

        sort_by = form.cleaned_data.get("sort_by")
        if sort_by:
            newspapers = newspapers.order_by(sort_by)
        elif query:
            newspapers = newspapers.order_by("-published_date")
        else:
            newspapers = newspapers.order_by("-published_date")

    paginator = Paginator(
        newspapers.select_related("topic").prefetch_related("publishers"), 12
    )
    page = request.GET.get("page")
    newspapers_page = paginator.get_page(page)

    context = {
        "form": form,
        "newspapers": newspapers_page,
        "query": query,
        "total_results": newspapers.count(),
        "page_obj": newspapers_page,
        "is_paginated": newspapers_page.has_other_pages(),
    }

    return render(request, "news/search_results.html", context)


# AJAX (prompts when user enters text)🔻
def search_autocomplete(request):
    query = request.GET.get("q", "")
    if len(query) < 2:
        return JsonResponse({"suggestions": []})

    newspapers = Newspaper.objects.filter(title__icontains=query, is_published=True)[:5]
    topics = Topic.objects.filter(name__icontains=query, is_active=True)[:3]
    authors = Redactor.objects.filter(
        Q(first_name__icontains=query)
        | Q(last_name__icontains=query)
        | Q(username__icontains=query),
        is_active_redactor=True,
    )[:3]

    suggestions = []

    for newspaper in newspapers:
        suggestions.append(
            {
                "type": "newspaper",
                "title": newspaper.title,
                "url": newspaper.get_absolute_url(),
                "icon": "newspaper",
            }
        )

    for topic in topics:
        suggestions.append(
            {
                "type": "topic",
                "title": f"Тема: {topic.name}",
                "url": topic.get_absolute_url(),
                "icon": "tag",
            }
        )

    for author in authors:
        suggestions.append(
            {
                "type": "author",
                "title": f"Автор: {author.full_name or author.username}",
                "url": reverse("news:redactor-detail", kwargs={"pk": author.pk}),
                "icon": "user",
            }
        )

    return JsonResponse({"suggestions": suggestions})
