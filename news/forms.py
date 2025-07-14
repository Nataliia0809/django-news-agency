from django import forms
from .models import Newspaper, Topic
from accounts.models import Redactor


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = ['title', 'content', 'published_date', 'topic', 'publishers']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter newspaper title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Enter newspaper content'
            }),
            'published_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'topic': forms.Select(attrs={
                'class': 'form-select'
            }),
            'publishers': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['publishers'].queryset = self.fields['publishers'].queryset.all()
        self.fields['publishers'].widget.attrs.update({'class': 'form-check-input'})


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter topic name'
            }),
        }

class RedactorForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["username", "email", "first_name", "last_name", "years_of_experience"]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
        }