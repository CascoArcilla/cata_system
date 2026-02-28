from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from tecnicas.models import Catador, SesionSensorial, Participacion
from utils import controller_error


class LoginSessionTesterController():
    tester: Catador
    session: SesionSensorial
    taster_participation: Participacion
    current_direcction = "forms_tester/subscribe_session.html"
    destinity_direcction = "cata_system:catador_init_session"
    context = {}

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
        self.context = {}
        if not self.session.activo:
            self.context["error"] = "La sesión no está activa actualmente"
            return render(request, self.current_direcction, self.context)

        if self.session.tecnica.repeticion == 1:
            try:
                self.taster_participation = Participacion.objects.get(
                    tecnica=self.session.tecnica, catador=self.tester)
                self.context["error"] = "Usted ya esta dentro de la sesión"
                return render(request, self.current_direcction, self.context)

            except Participacion.DoesNotExist:
                with transaction.atomic():
                    code_session = self.session.codigo_sesion
                    self.session = SesionSensorial.objects.select_for_update().get(
                        codigo_sesion=code_session)

                    max_testers = self.session.tecnica.limite_catadores
                    current_num_testers = Participacion.objects.filter(
                        tecnica=self.session.tecnica).count()

                    if current_num_testers >= max_testers:
                        self.context["error"] = "La sesión ha alcanzado el número máximo de catadores"
                        return render(request, self.current_direcction, self.context)

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
            self.context["error"] = "Ya no es posible ingresar a la sesión"
            return render(request, self.current_direcction, self.context)

    def validateEntryRataCata(self, request: HttpRequest):
        self.context = {}
        if not self.session.activo:
            self.context["error"] = "La sesión no está activa actualmente"
            return render(request, self.current_direcction, self.context)

        if self.session.tecnica.repeticion <= 1:
            try:
                self.taster_participation = Participacion.objects.get(
                    tecnica=self.session.tecnica, catador=self.tester)
                self.context["error"] = "Usted ya esta dentro de la sesión"
                return render(request, self.current_direcction, self.context)
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
            self.context["error"] = "Imposible acceder a esta sesión"
            return render(request, self.current_direcction, self.context)

    def validateEntryLimitTesters(self, request: HttpRequest):
        self.context = {}
        if not self.session.activo:
            self.context["error"] = "La sesión no está activa actualmente"
            return render(request, self.current_direcction, self.context)

        if self.session.tecnica.repeticion == 1:
            return self.entrySessionLimitTesters(request)

        else:
            self.context["error"] = "Ya no es posible ingresar a la sesión"
            return render(request, self.current_direcction, self.context)

    def validateEntryNapping(self, request: HttpRequest):
        self.context = {}
        if not self.session.activo:
            self.context["error"] = "La sesión no está activa actualmente"
            return render(request, self.current_direcction, self.context)

        if self.session.tecnica.repeticion == 0:
            return self.entrySessionLimitTesters(request)

        else:
            self.context["error"] = "Ya no es posible ingresar a la sesión"
            return render(request, self.current_direcction, self.context)

    def entrySessionLimitTesters(self, request: HttpRequest):
        try:
            self.taster_participation = Participacion.objects.get(
                tecnica=self.session.tecnica, catador=self.tester)
            self.context["error"] = "Usted ya esta dentro de la sesión"
            return render(request, self.current_direcction, self.context)

        except Participacion.DoesNotExist:
            try:
                with transaction.atomic():
                    code_session = self.session.codigo_sesion
                    self.session = SesionSensorial.objects.select_for_update().get(
                        codigo_sesion=code_session)

                    max_testers = self.session.tecnica.limite_catadores
                    current_num_testers = Participacion.objects.filter(
                        tecnica=self.session.tecnica).count()

                    if current_num_testers >= max_testers:
                        raise ValueError(
                            "La sesión ha alcanzado el número máximo de catadores")

                    self.taster_participation = Participacion.objects.create(
                        tecnica=self.session.tecnica,
                        catador=self.tester,
                        finalizado=False
                    )
                    params = {
                        "code_sesion": self.session.codigo_sesion
                    }
                    return redirect(reverse(self.destinity_direcction, kwargs=params))

            except ValueError as e:
                self.context["error"] = str(e)
                return render(request, self.current_direcction, self.context)
