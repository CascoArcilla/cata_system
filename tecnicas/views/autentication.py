from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from tecnicas.utils import general_error

@csrf_exempt
def autentication(req: HttpRequest):
    context_view = {}
    urls_technique = {
        "escalas": "cata_system:index_escalas",
        "rata": "cata_system:index_rata",
        "cata": "cata_system:index_cata",
        "perfil-ideal": "cata_system:index_perfil_ideal",
        "general": "cata_system:index",
    }

    if req.method == "GET":
        return render(req, "tecnicas/auth.html")
    elif req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")
        technique = req.POST.get("technique") or "escalas"

        user = authenticate(username=username, password=password)

        if user is not None and hasattr(user, "user_presentador"):
            login(req, user)
            req.session["technique_selected"] = technique
            return redirect(urls_technique[technique])

        else:
            context_view["error"] = "Credenciales inválidas o no es un Presentador"
            return render(req, "tecnicas/auth.html", context_view)
    else:
        return general_error("Método no permitido")
