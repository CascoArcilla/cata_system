from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import Producto, Participacion, Palabra, Calificacion, ListaPalabras, Dato
from controllers import ParticipacionController, PalabrasController, EscalaController
from tecnicas.forms import ListWordsForm
from .general_test_controller import GenetalTestController


class TestPFController(GenetalTestController):
    skip_phases = 2

    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)

    def controllGet(self, request: HttpRequest, error=""):
        self.participation = Participacion.objects.get(
            tecnica=self.session.tecnica, catador=request.user.user_catador)
        self.context["session"] = self.session

        if error:
            self.context["error"] = error

        rep = self.session.tecnica.repeticion

        if rep == 1:
            self.current_directory = "forms_tester/test_pf_list_words.html"
            response = self.getFirstPhase(request)
        elif rep == 2:
            self.current_directory = "forms_tester/test_pf_list_words.html"
            response = self.getSecondPhase(request)
        elif rep >= 3:
            self.current_directory = "forms_tester/test_pf_rating_list.html"
            response = self.getRepetitionPhase(request)
        else:
            response = self.getErrorRepetition(request)

        return response

    def controllPost(self, request: HttpRequest):
        action = request.POST["action"]

        if action == "finish_session":
            try:
                self.participation = Participacion.objects.get(
                    tecnica=self.session.tecnica, catador=request.user.user_catador)
            except Participacion.DoesNotExist:
                return self.controllGet(request, error="No se ha encontrado la participación")

            response = ParticipacionController.finishSession(
                self.participation)
            if isinstance(response, dict) and response.get("error"):
                return self.controllGet(request, error=response["error"])

            params = {"code_sesion": self.session.codigo_sesion}
            return redirect(reverse(self.previus_directory, kwargs=params))

        else:
            return self.controllGet(request, error="Acción no permitida")

    def getFirstPhase(self, request: HttpRequest):
        self.participation.refresh_from_db()

        if self.participation.finalizado:
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse(self.previus_directory, kwargs=params))

        self.context["form"] = ListWordsForm()
        self.context["initial_phase"] = True

        try:
            tester_list = ListaPalabras.objects.get(
                tecnica=self.session.tecnica,
                catador=request.user.user_catador,
                es_final=False
            )
            list_words = list(tester_list.palabras.all())
            self.context["words"] = list_words
        except ListaPalabras.DoesNotExist:
            self.context["words"] = []

        return render(request, self.current_directory, self.context)

    def getSecondPhase(self, request: HttpRequest):
        self.participation.refresh_from_db()

        if self.participation.finalizado:
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse(self.previus_directory, kwargs=params))

        try:
            tester_list = ListaPalabras.objects.get(
                tecnica=self.session.tecnica,
                catador=request.user.user_catador,
                es_final=True
            )
        except ListaPalabras.DoesNotExist:
            tester_list = ListaPalabras.objects.get(
                tecnica=self.session.tecnica,
                catador=request.user.user_catador,
                es_final=False
            )

        list_words = list(tester_list.palabras.all())

        self.context["form"] = ListWordsForm()
        self.context["initial_phase"] = False
        self.context["words"] = list_words

        return render(request, self.current_directory, self.context)

    def getRepetitionPhase(self, request: HttpRequest):
        '''
        - Obtener todos los productos que se evaluan en la tecnica
        - Obtener todas las palabras de la lista de palabras del catador
        - Para cada palabra, comprobar que el numero de Dato sea igual al numero de Productos
        - Si no hay datos mandar esa palabra por contexto con todos los productos
        - De las palabras que falten tomar la primera y mandarla en el contexto
        - Mandar todos los productos por el contexto
        Nota: Para esta fase no hay necesidad de mandar una escala, la escala se creara en el cliente
        '''
        self.participation.refresh_from_db()

        if self.participation.finalizado:
            params = {"code_sesion": self.session.codigo_sesion}
            return redirect(reverse(self.previus_directory, kwargs=params))

        technique = self.session.tecnica

        # Obtener todos los productos que se evaluan en la técnica
        products_in_technique = Producto.objects.filter(id_tecnica=technique)

        # Obtener todas las palabras de la lista del catador (preferir lista final)
        try:
            words = list(ListaPalabras.objects.get(
                tecnica=self.session.tecnica,
                catador=request.user.user_catador,
                es_final=True
            ).palabras.all())
        except ListaPalabras.DoesNotExist:
            words = []

        use_word: Palabra = None

        # Revisar que palabra no ha sido calificada en todos los productos
        for word in words:
            current_num_data = Dato.objects.filter(
                id_calificacion__num_repeticion=technique.repeticion,
                id_calificacion__id_tecnica=technique,
                id_calificacion__id_catador=request.user.user_catador,
                id_palabra=word
            ).count()

            if not current_num_data:
                use_word = word
                break
            elif current_num_data < len(products_in_technique):
                self.context["error"] = "Se ha detectado una inconsistencia en los datos que se deben calificar, algunos productos no han sido calificados"
                return render(request, self.current_directory, self.context)

        if not use_word:
            self.participation = Participacion.objects.get(
                tecnica=self.session.tecnica, catador=request.user.user_catador)
            ParticipacionController.finishSession(self.participation)
            params = {"code_sesion": self.session.codigo_sesion}
            return redirect(reverse(self.previus_directory, kwargs=params))

        self.context["word"] = use_word
        self.context["products"] = products_in_technique
        self.context["repetition"] = technique.repeticion - self.skip_phases

        return render(request, self.current_directory, self.context)

    def getErrorRepetition(self, request: HttpRequest):
        params = {
            "code_sesion": self.session.codigo_sesion
        }
        return redirect(reverse(self.previus_directory, kwargs=params))
