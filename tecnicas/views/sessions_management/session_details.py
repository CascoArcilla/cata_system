from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from ...controllers import DetallesSesionController


def sessionDetails(req: HttpRequest, session_code: str):
    context = DetallesSesionController.getContextForView(session_code)

    if req.method == "GET":
        return render(req, "tecnicas/manage_sesions/detalles-sesion.html", context)
    elif req.method == "POST":
        if req.POST["action"] == "start_session":
            response = DetallesSesionController.startRepetition(
                session_code, req.POST.get("username"))
            if isinstance(response, dict):
                context["error"] = response["error"]
                return render(req, "tecnicas/manage_sesions/detalles-sesion.html", context)

            return redirect(reverse("cata_system:----"))
        elif req.POST.get("action") == "delete_session":
            pass
        elif req.POST.get("action") == "monitor_session":
            pass
        else:
            context["error"] = "no se reconoce la accion a realizar"
            return render(req, "tecnicas/manage_sesions/detalles-sesion.html", context)
