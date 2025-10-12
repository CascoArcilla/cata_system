'''
Para finalizar la sesion se debe realizar lo siguiente
# Obtener todas las participaciones

'''

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.controllers import MonitorSesionController
from tecnicas.utils import general_error


def sessionMonitor(req: HttpRequest, session_code: str):
    controll_view = MonitorSesionController(session_code)
    context = controll_view.monitorView()

    if req.method == "GET":
        if "error" in context:
            return render(req, "tecnicas/manage_sesions/monitor-sesion.html", context)

        context["code_session"] = session_code
        return render(req, "tecnicas/manage_sesions/monitor-sesion.html", context)
    elif req.method == "POST":
        action = req.POST["action"]
        if action == "finish_session":
            return actionFinishSession(context=context, session_code=session_code, controll_view=controll_view, req=req)
        else:
            return general_error("No se ha especificado la acción")
    else:
        return JsonResponse({"error": "Método no permitido"})


def actionFinishSession(context: dict, session_code: str, controll_view: MonitorSesionController, req: HttpRequest):
    context["code_session"] = session_code
    (is_all_end, message) = controll_view.checkAllParticipantsEnded()
    context["message"] = message
    if not is_all_end:
        return render(req, "tecnicas/manage_sesions/monitor-sesion.html", context)
    response = controll_view.finishSession()
    if isinstance(response, dict):
        context["message"] = response["error"]
        return render(req, "tecnicas/manage_sesions/monitor-sesion.html", context)
    return redirect(reverse("cata_system:detalles_sesion", kwargs={"session_code": session_code}))
