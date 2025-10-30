from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from tecnicas.models import Catador, SesionSensorial, Participacion
from tecnicas.utils import controller_error


class LoginTesterController():
    tester: Catador
    session: SesionSensorial
    taster_participation: Participacion
    current_direcction = "tecnicas/forms_tester/login_session.html"
    destinity_direcction = "cata_system:catador_init_session"

    def __init__(self):
        self.tester = Catador()
        self.session = SesionSensorial()

    def existCredential(self, user_tester: str, code_session: str):
        try:
            self.tester = Catador.objects.get(user__username=user_tester)
            self.session = SesionSensorial.objects.get(
                codigo_sesion=code_session)

            return (self.tester, self.session)
        except (Catador.DoesNotExist, SesionSensorial.DoesNotExist):
            return controller_error("Credenciales inválidas")

    def validateEntryEscalas(self, request=HttpRequest):
        context = {}
        if not self.session.activo:
            context["error"] = "La sesión no está activa actualmente"
            return render(request, self.current_direcction, context)

        if self.session.tecnica.repeticion > 1:
            try:
                self.taster_participation = Participacion.objects.get(
                    tecnica=self.session.tecnica, catador=self.tester)
                context["error"] = "Usted ya esta dentro de la sesión"
                return render(request, self.current_direcction, context)
            except Participacion.DoesNotExist:
                context["error"] = "No tienes permitido entrar a esta sesión"
                return render(request, self.current_direcction, context)
        else:
            with transaction.atomic():
                code_session = self.session.codigo_sesion
                self.session = SesionSensorial.objects.select_for_update().get(
                    codigo_sesion=code_session)

                max_testers = self.session.tecnica.limite_catadores
                current_num_testers = Participacion.objects.filter(
                    tecnica=self.session.tecnica).count()

                if current_num_testers >= max_testers:
                    context["error"] = "La sesión ha alcanzado el número máximo de catadores"
                    return render(request, self.current_direcction, context)

                self.taster_participation = Participacion.objects.create(
                    tecnica=self.session.tecnica,
                    catador=self.tester,
                    finalizado=False
                )
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse(self.destinity_direcction, kwargs=params))

    def validateEntryRATA(self, request: HttpRequest):
        context = {}
        if not self.session.activo:
            context["error"] = "La sesión no está activa actualmente"
            return render(request, self.current_direcction, context)

        if self.session.tecnica.repeticion <= 1:
            try:
                self.taster_participation = Participacion.objects.get(
                    tecnica=self.session.tecnica, catador=self.tester)
                context["error"] = "Usted ya esta dentro de la sesión"
                return render(request, self.current_direcction, context)
            except Participacion.DoesNotExist:
                with transaction.atomic():
                    code_session = self.session.codigo_sesion
                    self.session = SesionSensorial.objects.select_for_update().get(
                        codigo_sesion=code_session)

                    self.taster_participation = Participacion.objects.create(
                        tecnica=self.session.tecnica,
                        catador=self.tester,
                        finalizado=False
                    )

                params = {
                    "code_sesion": self.session.codigo_sesion
                }
                return redirect(reverse(self.destinity_direcction, kwargs=params))
        else:
            context["error"] = "Imposible acceder a esta sesión"
            return render(request, self.current_direcction, context)
