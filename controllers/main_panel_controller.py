from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from utils import general_error
from tecnicas.models import Presentador, SesionSensorial


class PanelMainCotroller:
    def __init__(self, template: str, filter_sesion: dict):
        self.template = template
        self.filter_sesion = filter_sesion

    def get(self, req: HttpRequest):
        user = req.user
        try:
            presentador = Presentador.objects.get(user=user)
            telefono = presentador.telefono
        except Presentador.DoesNotExist:
            presentador = None
            telefono = "No registrado"

        if presentador:
            total_sessions = SesionSensorial.objects.filter(
                creadoPor=presentador, **self.filter_sesion).count()
            active_sessions = SesionSensorial.objects.filter(
                creadoPor=presentador, activo=True, **self.filter_sesion).count()
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
        return render(req, self.template, context=context_view)

    def post(self, req: HttpRequest):
        action = req.POST.get("action")
        if action == "exit_session":
            logout(req)
            return redirect("analist:login_analista")
        else:
            general_error("Acción no definida")
