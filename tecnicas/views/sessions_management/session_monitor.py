from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from tecnicas.controllers import MonitorSesionController


def sessionMonitor(req: HttpRequest, session_code: str):
    if req.method == "GET":
        controll_view = MonitorSesionController(session_code)

        context = controll_view.monitorView()
        if "error" in context:
            return render(req, "tecnicas/manage_sesions/monitor-sesion.html", context)
        
        context["code_session"] = session_code
        return render(req, "tecnicas/manage_sesions/monitor-sesion.html", context)
    else:
        return JsonResponse({"error": "Método no permitido"})
