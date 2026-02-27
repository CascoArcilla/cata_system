from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from tecnicas.utils import general_error

@csrf_exempt
def autentication(req: HttpRequest, name_tecnica:str = None):
    context_view = {}
    urls_technique = {
        "escalas": "cata_system:index_escalas",
        "rata": "cata_system:index_rata",
        "cata": "cata_system:index_cata",
        "perfil-flash": "cata_system:index_perfil_flash",
        "sort": "cata_system:index_sort",
        "napping": "cata_system:index_napping",
        "perfil-ideal": "cata_system:index_ideal",
        "general": "cata_system:index",
    }

    if req.method == "GET":
        return render(req, "tecnicas/auth.html")
    elif req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

        if name_tecnica:
            technique = name_tecnica
        else:
            technique = req.GET.get("technique") or "escalas"

        if technique not in urls_technique:
            context_view["error"] = "Técnica no válida"
            return render(req, "tecnicas/auth.html", context_view)
        else:
            url_main = urls_technique.get(technique)

        user = authenticate(username=username, password=password)

        if user is not None and hasattr(user, "user_presentador"):
            login(req, user)
            req.session["technique_selected"] = technique
            req.session["sensorial_url_main"] = url_main
            return redirect(url_main)

        else:
            context_view["error"] = "Credenciales inválidas o no es un Presentador"
            return render(req, "tecnicas/auth.html", context_view)
    else:
        return general_error("Método no permitido")
