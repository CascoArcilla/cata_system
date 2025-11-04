from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Catador, SesionSensorial, Orden, Participacion, Producto, EsAtributo, Calificacion, EsVocabulario, Dato
from tecnicas.controllers import ParticipacionController
from tecnicas.utils import controller_error, shuffleArray


class InitSessionTesterController():
    tester: Catador
    session: SesionSensorial
    order: Orden | dict
    current_direction = "tecnicas/forms_tester/init_session.html"
    escalas_direction = "cata_system:session_convencional"

    def __init__(self, sensorial_session: SesionSensorial, user_tester: Catador):
        self.tester = user_tester
        self.session = sensorial_session

    def controllGetEscalas(self, request: HttpRequest):
        context = {
            "session": self.session,
            "type_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        order = self.checkAndAssignOrder()
        if isinstance(order, dict):
            context["error"] = order["error"]
            return render(request, self.current_direction, context)

        is_end = self.isEndedSessionEscalas()

        request.session["id_order"] = order.id
        context["has_ended"] = is_end

        if is_end:
            context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"

        if "error" in request.GET:
            context["error"] = request.GET["error"]

        return render(request, self.current_direction, context)

    def controllPostEscalas(self, request: HttpRequest):
        context = {
            "session": self.session,
            "type_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        if request.POST["action"] == "start_posting":
            parameters = {
                "code_sesion": self.session.codigo_sesion
            }

            is_end = self.isEndedSessionEscalas()
            if is_end:
                context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"
                return render(request, self.current_direction, context)

            update_participation = ParticipacionController.enterSession(
                tester=request.user.user_catador, session=self.session)
            if isinstance(update_participation, dict):
                context["error"] = update_participation["error"]
                return render(request, self.current_direction, context)

            request.session["id_participation"] = update_participation.id
            return redirect(reverse(self.escalas_direction, kwargs=parameters))
        elif request.POST["action"] == "exit_session":
            response = ParticipacionController.outSession(
                tester=request.user.user_catador, session=self.session)
            if isinstance(response, dict):
                context["error"] = response["error"]
            return render(request, self.current_direction, context)
        else:
            context["error"] = "Acción sin especificar"
            return render(request, self.current_direction, context)

    def controllGetRATA(self, request: HttpRequest):
        context = {
            "session": self.session,
            "type_technique": self.session.tecnica.tipo_tecnica.nombre_tecnica
        }

        is_end = self.isEndedSessionEscalas()

        context["has_ended"] = is_end

        if is_end:
            context["message"] = "El catador ha terminado de realizar su evaluación, espere instrucciones del presentador"

        return render(request, self.current_direction, context)

    def assignOrder(self):
        with transaction.atomic():
            orders_without_tester = list(Orden.objects.select_for_update().filter(
                id_tecnica=self.session.tecnica, id_catador=None))

            if not orders_without_tester:
                return controller_error("Las ordenes se han acabado")

            shuffle_orders = shuffleArray(orders_without_tester)
            self.order_to_assign = shuffle_orders.pop()

            self.order_to_assign.id_catador = self.tester
            self.order_to_assign.save()

            return self.order_to_assign

    def checkAndAssignOrder(self):
        try:
            self.order_to_assign = Orden.objects.get(
                id_tecnica=self.session.tecnica, id_catador=self.tester)
        except Orden.DoesNotExist:
            create = self.assignOrder()
            if isinstance(create, dict):
                return create
        return self.order_to_assign

    def isEndedSessionEscalas(self):
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

                technique = self.session.tecnica
                style_words = technique.id_estilo.nombre_estilo

                num_words: int

                if style_words == "atributos":
                    num_words = EsAtributo.objects.get(
                        id_tecnica=self.session.tecnica).palabras.count()
                elif style_words == "vocabulario":
                    num_words = EsVocabulario.objects.get(
                        id_tecnica=self.session.tecnica).id_vocabulario.palabras.count()

                expected_ratings_repetition = num_products * num_words

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
            return controller_error("No se ha encontrado la participación")
