from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from ...controllers import DetallesSesionController


def sessionDetails(req: HttpRequest, session_code: str):
    controller_view = DetallesSesionController(session_code)
    context = controller_view.getContextForView()

    if req.method == "GET":
        context = controller_view.getContextWithData()
        return render(req, "tecnicas/manage_sesions/detalles-sesion.html", context)
    elif req.method == "POST":
        if req.POST["action"] == "start_session":
            response = DetallesSesionController.startRepetition(
                session_code=session_code, username=req.user.username)
            if isinstance(response, dict):
                context = controller_view.getContextWithData()
                context["error"] = response["error"]
                return render(req, "tecnicas/manage_sesions/detalles-sesion.html", context)

            parameters = {
                "session_code": controller_view.session.codigo_sesion
            }

            return redirect(reverse("cata_system:monitor_sesion", kwargs=parameters))
        elif req.POST.get("action") == "delete_session":
            pass
        else:
            context["error"] = "no se reconoce la accion a realizar"
            return render(req, "tecnicas/manage_sesions/detalles-sesion.html", context)
