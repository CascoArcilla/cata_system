from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from tecnicas.utils import general_error


def mainPanel(req: HttpRequest):
    if req.method == "GET":
        context_view = {
            "name": f"{req.user.first_name} {req.user.last_name}",
            "username": f"{req.user.username}"
        }
        return render(req, "tecnicas/main-panel.html", context=context_view)
    elif req.method == "POST":
        action = req.POST["action"]
        if action == "exit_session":
            logout(req)
            return redirect("cata_system:autenticacion")
        else:
            general_error("Acción no definida")
    else: 
        general_error("Método no permitido")
