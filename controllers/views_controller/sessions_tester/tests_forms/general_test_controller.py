from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from tecnicas.models import SesionSensorial, Catador, Participacion
from controllers import ParticipacionController


class GenetalTestController():
    previus_directory = "cata_system:catador_init_session"
    context = {}
    current_directory: str

    def __init__(self, sensorial_session: SesionSensorial, user_tester: Catador):
        self.tester = user_tester
        self.session = sensorial_session

    def controllPost(self, request: HttpRequest):
        action = request.POST["action"]

        if action == "finish_session":
            self.participation = Participacion.objects.get(
                tecnica=self.session.tecnica, catador=request.user.user_catador)
            ParticipacionController.finishSession(self.participation)
            params = {"code_sesion": self.session.codigo_sesion}
            return redirect(reverse(self.previus_directory, kwargs=params))

        else:
            return self.controllGet(request, error="Acción no permitida")
