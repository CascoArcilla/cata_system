from django.http import HttpRequest
from django.shortcuts import render
from .init_session_controller import InitSessionController


class InitSessionRATAController(InitSessionController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_direction = "forms_tester/init_rata_test.html"

    def controllGet(self, request: HttpRequest):
        context = {
            "session_info": {
                "code": self.session.codigo_sesion,
                "name": self.session.nombre_sesion,
                "instructions": self.session.tecnica.instrucciones,
                "style": self.session.tecnica.id_estilo.nombre_estilo
            },
            "use_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        try:
            context["session_info"]["type_scale"] = self.session.tecnica.escala_tecnica.first().id_tipo_escala.nombre_escala
        except AttributeError:
            context["session_info"]["type_scale"] = None

        is_end = self.isEndedSession()

        context["has_ended"] = is_end

        if is_end:
            context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del analista"

        return render(request, self.current_direction, context)
