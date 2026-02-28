from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Catador, SesionSensorial, Participacion, Producto, EsAtributo, EsVocabulario, Dato, DatoHedonico
from controllers import ParticipacionController, PalabrasController
from .init_session_controller import InitSessionController


class InitSessionPerfilIdealController(InitSessionController):
    tester: Catador
    session: SesionSensorial

    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_direction = "tecnicas/forms_tester/init_perfil_ideal_test.html"

    def controllGet(self, request: HttpRequest, from_post: bool | str = False):
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

        is_end = self.isEndedSession()
        if is_end:
            context["has_ended"] = True

        if "error" in request.GET:
            context["error"] = request.GET["error"]

        if from_post:
            context["error"] = from_post
            return context

        return render(request, self.current_direction, context)

    def controllPost(self, request: HttpRequest):
        use_action = request.POST["action"] or None

        if use_action == "start_posting":
            is_end = self.isEndedSession()
            if is_end:
                return self.controllGet(request=request, from_post="Has terminado de realizar tu evaluación, espera instrucciones del Analista")

            update_participation = ParticipacionController.enterSession(
                tester=request.user.user_catador, session=self.session)
            if isinstance(update_participation, dict):
                return self.controllGet(request=request, from_post=update_participation["error"])

            request.session["id_participation"] = update_participation.id
            return redirect(reverse("cata_system:session_perfil_ideal_phase1", args=[self.session.codigo_sesion]))

        elif use_action == "exit_session":
            response = ParticipacionController.outSession(
                tester=request.user.user_catador, session=self.session)
            if isinstance(response, dict):
                return self.controllGet(request=request, from_post=response["error"])
            return self.controllGet(request=request)

        else:
            return self.controllGet(request=request, from_post="Acción sin especificar")

    def isEndedSession(self):
        try:
            participation = Participacion.objects.get(
                catador=self.tester, tecnica=self.session.tecnica)
            self.session.refresh_from_db()

            # ////////////////////////////////////////////////////////////// #
            #
            # numero de datos de escala intensidad como ideal = numero_de_palabras * numero_de_productos
            # numero de datos de escala preferencia = numero_de_productos
            #
            # ////////////////////////////////////////////////////////////// #

            if participation.finalizado:
                num_products = Producto.objects.filter(
                    id_tecnica=self.session.tecnica).count()

                technique = self.session.tecnica
                style_words = technique.id_estilo.nombre_estilo

                num_words = len(PalabrasController.getWordsInTechnique(technique=technique))

                end_phase1 = InitSessionPerfilIdealController.endPhase1(
                    num_words, num_products, participation)

                end_phase2 = InitSessionPerfilIdealController.endPhase2(
                    num_products, participation)

                return end_phase1[0] and end_phase2[0]
            else:
                return participation.finalizado
        except Participacion.DoesNotExist:
            return controller_error("No se ha encontrado la participación")

    @staticmethod
    def endPhase1(num_words: int, num_products: int, participation: Participacion) -> tuple[bool, str]:
        # ////////////////////////////////////////////////////////////// #
        # numero de datos de escala intensidad como ideal = numero_de_palabras * numero_de_productos
        # ////////////////////////////////////////////////////////////// #
        expected_data_intensity_ideal = num_products * num_words

        participation.refresh_from_db()

        current_data_intensity = Dato.objects.filter(
            id_calificacion__id_catador=participation.catador,
            id_calificacion__id_tecnica=participation.tecnica,
            id_calificacion__num_repeticion=1,
            id_calificacion__calificacion_escala__escala__id_tipo_escala__nombre_escala="estructurada"
        ).count()

        current_data_ideal = Dato.objects.filter(
            id_calificacion__id_catador=participation.catador,
            id_calificacion__id_tecnica=participation.tecnica,
            id_calificacion__num_repeticion=1,
            id_calificacion__calificacion_escala__escala__id_tipo_escala__nombre_escala="ideal"
        ).count()

        is_end = (current_data_intensity == current_data_ideal ==
                  expected_data_intensity_ideal)

        result = tuple()

        if is_end:
            result = (True, "Fase 1 completada")
        else:
            result = (False, "Fase 1 no completada")

        return result

    @staticmethod
    def endPhase2(num_products: int, participation: Participacion) -> tuple[bool, str]:
        # ////////////////////////////////////////////////////////////// #
        # numero de datos de escala preferencia = numero_de_productos
        # ////////////////////////////////////////////////////////////// #
        expected_data_preference = num_products

        participation.refresh_from_db()

        current_data_preference = DatoHedonico.objects.filter(
            calificacion__id_catador=participation.catador,
            calificacion__id_tecnica=participation.tecnica,
            calificacion__num_repeticion=1,
        ).count()

        is_end = (current_data_preference == expected_data_preference)

        result = tuple()

        if is_end:
            result = (True, "Fase 2 completada")
        else:
            result = (False, "Fase 2 no completada")

        return result
