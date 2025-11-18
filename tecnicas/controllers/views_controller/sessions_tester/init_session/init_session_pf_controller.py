from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Participacion, Producto, Dato, ListaPalabras
from tecnicas.controllers import ParticipacionController
from .init_session_controller import InitSessionController


class InitSessionPFController(InitSessionController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_direction = "tecnicas/forms_tester/init_session_pf.html"
        self.pf_direction = "cata_system:session_pf"

    def controllGet(self, request: HttpRequest):
        context = {
            "session": self.session,
            "type_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        (is_end, message, rep_show) = self.isEndedSession()

        context["has_ended"] = is_end
        context["activity"] = message
        context["repetition"] = rep_show

        if "error" in request.GET:
            context["error"] = request.GET["error"]

        return render(request, self.current_direction, context)

    def controllPost(self, request: HttpRequest):
        context = {
            "session": self.session,
            "type_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        action = request.POST["action"]

        if action == "start_posting":
            parameters = {
                "code_sesion": self.session.codigo_sesion
            }

            (is_end, message, rep_show) = self.isEndedSession()
            if is_end:
                return self.controllGet(request)

            update_participation = ParticipacionController.enterSession(
                tester=request.user.user_catador, session=self.session)
            if isinstance(update_participation, dict):
                context["error"] = update_participation["error"]
                return render(request, self.current_direction, context)

            request.session["id_participation"] = update_participation.id

            return redirect(reverse(self.pf_direction, kwargs=parameters))

        elif action == "exit_session":
            response = ParticipacionController.outSession(
                tester=request.user.user_catador, session=self.session)
            if isinstance(response, dict):
                context["error"] = response["error"]
            return self.controllGet(request)

        else:
            context["error"] = "Acción sin especificar"
            return render(request, self.current_direction, context)

    def isEndedSession(self) -> tuple[bool, str, int]:
        rep = self.session.tecnica.repeticion

        is_end = False
        message = ""
        repetitiom_show = 0

        if rep == 1:
            is_end = self.endedSessionMakeList()
            message = "Ya has creado la Lista de palabras inicial" if is_end else "Debes crear tu lista de palabras inicial"
            repetitiom_show = 0
        elif rep == 2:
            is_end = self.endedSessionMakeList()
            message = "Ya has creado la Lista de palabras final" if is_end else "Debes crear tu lista de palabras final"
            repetitiom_show = 0
        elif rep >= 3:
            is_end = self.endedSessionRepetition()
            message = "Has finalizado con el proceso de calificación" if is_end else "Debe hacer tu proceso de calificación"
            repetitiom_show = rep - 2
        else:
            message = "Parece que la repetición es cero, no es posible hacer algo ahora mismo"

        return (is_end, message, repetitiom_show)

    def endedSessionMakeList(self):
        try:
            return Participacion.objects.get(
                catador=self.tester, tecnica=self.session.tecnica).finalizado
        except Participacion.DoesNotExist:
            print("No se ha encontrado la participación")
            return False

    def endedSessionRepetition(self):
        try:
            participation = Participacion.objects.get(
                catador=self.tester, tecnica=self.session.tecnica)
            self.session.refresh_from_db()

            # ////////////////////////////////////////////////////////////// #
            #
            # numero_datos_esperadas = num_productos * num_palabras
            # Si numero_datos_esperadas es igual a numero_datos_actuales en la repetcion R
            # Ha terminado la repeticion
            #
            # ////////////////////////////////////////////////////////////// #

            if participation.finalizado:
                num_products = Producto.objects.filter(
                    id_tecnica=self.session.tecnica).count()

                num_words = ListaPalabras.objects.get(
                    tecnica=self.session.tecnica,
                    catador=self.tester,
                    es_final=True
                ).palabras.all().count()

                expected_ratings_repetition = num_products * num_words

                technique = self.session.tecnica
                num_ratings_now = Dato.objects.filter(
                    id_calificacion__id_catador=self.tester,
                    id_calificacion__id_tecnica=technique,
                    id_calificacion__num_repeticion=technique.repeticion
                ).count()

                is_end = num_ratings_now >= expected_ratings_repetition

                return is_end

            else:
                return participation.finalizado

        except Participacion.DoesNotExist:
            print("No se ha encontrado la participación")
            return False
