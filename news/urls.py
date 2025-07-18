# написати news/urls і для accounts views і urls
from django.urls import path
from . import views

app_name = "news"

urlpatterns = [

    # home page🔻
    path("", views.index, name="index"),

    # newspapers🔻
    path("newspapers/", views.NewspaperListView.as_view(), name="newspaper-list"),
    path(
        "newspapers/<int:pk>/",
        views.NewspaperDetailView.as_view(),
        name="newspaper-detail",
    ),
    path(
        "newspapers/create/",
        views.NewspaperCreateView.as_view(),
        name="newspaper-create",
    ),
    path(
        "newspapers/<int:pk>/update/",
        views.NewspaperUpdateView.as_view(),
        name="newspaper-update",
    ),
    path(
        "newspapers/<int:pk>/delete/",
        views.NewspaperDeleteView.as_view(),
        name="newspaper-delete",
    ),

    # topics🔻
    path("topics/", views.TopicListView.as_view(), name="topic-list"),
    path("topics/<int:pk>/", views.TopicDetailView.as_view(), name="topic-detail"),
    path("topics/create/", views.TopicCreateView.as_view(), name="topic-create"),

    # redactors🔻
    path("redactors/", views.RedactorListView.as_view(), name="redactor-list"),
    path(
        "redactors/<int:pk>/",
        views.RedactorDetailView.as_view(),
        name="redactor-detail",
    ),
    # search🔻
    path("search/", views.search_view, name="search"),
    path("search/autocomplete/", views.search_autocomplete, name="search-autocomplete"),
]
