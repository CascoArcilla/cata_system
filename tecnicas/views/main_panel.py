from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from tecnicas.utils import general_error
from tecnicas.models import Presentador, SesionSensorial


def mainPanel(req: HttpRequest):
    if req.method == "GET":
        user = req.user
        try:
            presentador = Presentador.objects.get(user=user)
            telefono = presentador.telefono
        except Presentador.DoesNotExist:
            presentador = None
            telefono = "No registrado"

        if presentador:
            total_sessions = SesionSensorial.objects.filter(creadoPor=presentador).count()
            active_sessions = SesionSensorial.objects.filter(creadoPor=presentador, activo=True).count()
        else:
            total_sessions = 0
            active_sessions = 0

        context_view = {
            "name": f"{user.first_name} {user.last_name}",
            "username": f"{user.username}",
            "email": user.email,
            "telefono": telefono,
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
        }
        return render(req, "tecnicas/main-panel.html", context=context_view)
    elif req.method == "POST":
        action = req.POST.get("action")
        if action == "exit_session":
            logout(req)
            return redirect("cata_system:autenticacion")
        else:
            general_error("Acción no definida")
    else: 
        general_error("Método no permitido")
