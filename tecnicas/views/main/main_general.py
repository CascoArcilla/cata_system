from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from tecnicas.utils import general_error
from tecnicas.models import Presentador, SesionSensorial
from django.urls import reverse
from django.utils.http import urlencode


def mainPanel(req: HttpRequest):
    if req.method == "GET":
        context = get_context_main(req)
        template = "tecnicas/mains_panels/main-panel.html"
        return render(req, template, context=context)

    elif req.method == "POST":
        return post_main(req)
    else:
        return general_error("Método no permitido")


def get_context_main(req: HttpRequest, more_filter: dict = {}):
    user = req.user

    try:
        presentador = Presentador.objects.get(user=user)
        telefono = presentador.telefono
    except Presentador.DoesNotExist:
        presentador = None
        telefono = "No registrado"

    if presentador:
        total_sessions = SesionSensorial.objects.filter(
            creadoPor=presentador, **more_filter).count()
        active_sessions = SesionSensorial.objects.filter(
            creadoPor=presentador, activo=True, **more_filter).count()
    else:
        total_sessions = 0
        active_sessions = 0

    context = {
        "name": f"{user.first_name} {user.last_name}",
        "username": f"{user.username}",
        "email": user.email,
        "telefono": telefono,
        "total_sessions": total_sessions,
        "active_sessions": active_sessions,
    }

    if req.GET.get("error"):
        context["error"] = req.GET.get("error")

    return context


def post_main(
    req: HttpRequest,
    technique=None,
    current_template: str = "tecnicas/mains_panels/main-panel.html",
    more_filter: dict = {}
):
    action = req.POST.get("action")
    if action == "exit_session":
        logout(req)
        base_url = reverse("cata_system:autenticacion")

        technique_use = req.POST.get("technique")

        if technique:
            query_string = urlencode({"technique": technique})
            return redirect(f"{base_url}?{query_string}")

        return redirect("cata_system:autenticacion")
    else:
        context = get_context_main(req, more_filter=more_filter)
        return render(req, current_template, context=context)
