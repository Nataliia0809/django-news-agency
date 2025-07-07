from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Newspaper, Topic
from .forms import NewspaperForm, TopicForm
from accounts.models import Redactor

#гол сторінка🔻
def index(request):
    newspapers = Newspaper.objects.all()[:5]
    context = {
        "newspapers": newspapers,
        "total_newspapers": Newspaper.objects.count(),
        "total_topics": Topic.objects.count(),
        "total_redactors": Redactor.objects.count()
    }

    return render(request, 'news/index.html', context)

#газета🔻
class NewspaperListView(ListView):
    model = Newspaper
    template_name = 'news/newspaper_list.html'
    context_object_name = 'newspapers'
    paginate_by = 10

    def get_queryset(self):
        queryset = Newspaper.objects.select_related('topic'). prefetch_related("publishers")
        topic_id = self.request.GET.get("topic")
        if topic_id:
            queryset = queryset.filter(topic__id=topic_id)
        return queryset

    def context_data(self, **kwargs):
        context = super() .get_context_data(**kwargs)
        context[topics] = Topic.objects.all()
        context["selected_topic"] = self.request.GET.get("topic")
        return context

class NewspaperDetailView(DetailView):
    model = Newspaper
    template_name = 'news/newspaper_detail.html'

class NewspaperCreateView(LoginRequiredMixin, CreateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = 'news/newspaper_create.html'

class NewspaperUpdateView(LoginRequiredMixin, UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = 'news/newspaper_update.html'

class NewspaperDeleteView(LoginRequiredMixin, DeleteView):
    model = Newspaper
    template_name = 'news/newspaper_delete.html'
    success_url = reverse_lazy("news:newspaper-list")

#Теми🔻
class TopicListView(ListView):
    model = Topic
    template_name = "news/topic_list.html"

class TopicDetailView(DetailView):
    model = Topic
    template_name = news/topic_detail.html

    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ["newspapers"] = self.object.newspaper.all
        return context

class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "news/topic_create.html"

#редактори🔻
class RedactorCreateView(LoginRequiredMixin, CreateView):
    model = Redactor
    form_class = RedactorForm
    template_name = "news/redactor_create.html"

class RedactorDetailView(DetailView):
    model = Redactor
    form_class = Redactorform
    template_name = "news/redactor_detail.html"



