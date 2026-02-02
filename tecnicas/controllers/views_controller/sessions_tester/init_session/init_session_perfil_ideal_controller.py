from django.http import HttpRequest
from django.shortcuts import render
from tecnicas.models import Catador, SesionSensorial
from .init_session_controller import InitSessionController


class InitSessionPerfilIdealController(InitSessionController):
    tester: Catador
    session: SesionSensorial

    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_direction = "tecnicas/forms_tester/init_perfil_ideal_test.html"

    def controllGet(self, request: HttpRequest, from_post:bool|str=False):
        context = {
            "session_info": {
                "code": self.session.codigo_sesion,
                "name": self.session.nombre_sesion,
                "instructions": self.session.tecnica.instrucciones,
                "style": self.session.tecnica.id_estilo.nombre_estilo,
                "activity": "Puntuación con escalas"
            },
            "use_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica,
            "has_ended": False
        }

        if "error" in request.GET:
            context["error"] = request.GET["error"]

        if from_post:
            context["error"] = from_post
            return context

        return render(request, self.current_direction, context)

    def controllPost(self, request: HttpRequest):
        context = self.controllGet(request, from_post="Esta funcionalidad está en desarrollo. Pronto podrás participar en sesiones de Perfil Ideal")
        return render(request, self.current_direction, context)
