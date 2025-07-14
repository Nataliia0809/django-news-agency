from django import forms
from .models import Newspaper, Topic
from accounts.models import Redactor


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ["title", "content", "published_date", "topic", "publishers"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter newspaper title"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Enter newspaper content",
                }
            ),
            "published_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "topic": forms.Select(attrs={"class": "form-select"}),
            "publishers": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["publishers"].queryset = self.fields["publishers"].queryset.all()
        self.fields["publishers"].widget.attrs.update({"class": "form-check-input"})


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter topic name"}
            ),
        }


class RedactorForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["username", "email", "first_name", "last_name", "years_of_experience"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter username"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter email"}
            ),
        }


# 🔻пошук
class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Пошук новин, авторів, тем...",
                "autocomplete": "off",
            }
        ),
        required=False,
    )

    topic = forms.ModelChoiceField(
        queryset=Topic.objects.filter(is_active=True),
        empty_label="Всі теми",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    author = forms.ModelChoiceField(
        queryset=Redactor.objects.filter(is_active_redactor=True),
        empty_label="Всі автори",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    priority = forms.ChoiceField(
        choices=[("", "Всі пріоритети")] + Newspaper.PRIORITY_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    sort_by = forms.ChoiceField(
        choices=[
            ("", "За релевантністю"),
            ("-published_date", "За датою (нові спочатку)"),
            ("published_date", "За датою (старі спочатку)"),
            ("-views_count", "За популярністю"),
            ("title", "За алфавітом"),
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
