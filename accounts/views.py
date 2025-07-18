from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import RedactorCreationForm


def signup(request):
    if request.method == "POST":
        form = RedactorCreationForm(request.POST)
        # 🔻check if all fields correctly field;
        # automatically enter the homepage as new user
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("news:index")
        else:
            form = RedactorCreationForm()
        return render(request, "registration/signup.html", {"form": form})
