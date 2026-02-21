from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from utils import general_error


@csrf_exempt
def login_analist(req: HttpRequest):
    context_view = {}
    urls = {
        "escalas": "analist:scales:main_escalas",
    }

    if req.method == "GET":
        return render(req, "analist/login.html")
    elif req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")
        technique = req.GET.get("technique") or "escalas"

        user = authenticate(username=username, password=password)

        if user is not None and hasattr(user, "user_presentador"):
            login(req, user)
            name_url = urls.get(technique)
            req.session["technique_use"] = technique
            return redirect(name_url)
        else:
            context_view["error"] = "Credenciales inválidas o no es un Presentador"
            return render(req, "analist/login.html", context_view)
    else:
        return general_error("Método no permitido")
