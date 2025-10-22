from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User


def loginTester(req: HttpRequest):
    if req.method == "GET":
        return render(req, "tecnicas/cata-login.html")
    elif req.method == "POST":
        view_context = {}
        username = req.POST.get("user_tester")

        user = User.objects.filter(username=username).first()
        if not user:
            view_context["error"] = "Catador no encontrado"
            return render(req, "tecnicas/cata-login.html", view_context)

        login(req, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(reverse("cata_system:catador_main"))
