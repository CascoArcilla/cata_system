from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from utils import general_error
from tecnicas.models import Presentador, SesionSensorial, TipoTecnica
from django.urls import reverse
from django.utils.http import urlencode
from tecnicas.decorators import required_technique


@required_technique("general")
def mainPanel(req: HttpRequest):
    if req.method == "GET":
        context = get_context_main(req)
        template = "mains_panels/main-panel.html"
        return render(req, template, context=context)

    elif req.method == "POST":
        return post_main(req)
    else:
        return general_error("Método no permitido")


def get_context_main(req: HttpRequest, more_filter: dict = {}, name_technique: str = "general"):
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

    try:
        tipo_tecnica = TipoTecnica.objects.get(
            nombre_tecnica=name_technique).descripcion
    except TipoTecnica.DoesNotExist:
        tipo_tecnica = "general"

    context = {
        "name": f"{user.first_name} {user.last_name}",
        "username": f"{user.username}",
        "email": user.email,
        "telefono": telefono,
        "total_sessions": total_sessions,
        "active_sessions": active_sessions,
        "technique": tipo_tecnica
    }

    if req.GET.get("error"):
        context["error"] = req.GET.get("error")

    return context


def post_main(
    req: HttpRequest,
    current_template: str = "mains_panels/main-panel.html",
    more_filter: dict = {},
    name_technique: str = "general"
):
    action = req.POST.get("action")
    if action == "exit_session":
        technique_use = req.session.get("technique_selected")
        base_url = reverse("cata_system:autenticacion")

        logout(req)
        if technique_use != "general":
            query_string = urlencode({"technique": technique_use})
            return redirect(f"{base_url}?{query_string}")

        return redirect(base_url)

    else:
        context = get_context_main(
            req, more_filter=more_filter, name_technique=name_technique)
        return render(req, current_template, context=context)
