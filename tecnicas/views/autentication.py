from django.contrib.auth import authenticate, login
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from tecnicas.utils import general_error
from tecnicas.models import Presentador

@csrf_exempt
def autentication(req: HttpRequest):
    context_view = {}

    if req.method == "GET":
        return render(req, "tecnicas/auth.html")
    elif req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None and hasattr(user, "user_presentador"):
            login(req, user)
            return redirect("cata_system:index")
        else:
            return JsonResponse({
                "success": False,
                "error": "Credenciales inválidas o no es un Presentador"
            })
    else:
        return general_error("Método no permitido")
