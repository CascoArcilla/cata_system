from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import Producto, Participacion, Palabra, Calificacion, ListaPalabras
from tecnicas.controllers import ParticipacionController, PalabrasController
from tecnicas.forms import ListWordsForm
from .general_test_controller import GenetalTestController


class TestPFController(GenetalTestController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)

    def controllGet(self, request: HttpRequest):
        self.participation = Participacion.objects.get(
            tecnica=self.session.tecnica, catador=request.user.user_catador)
        self.context["session"] = self.session

        rep = self.session.tecnica.repeticion

        if rep == 1:
            self.current_directory = "tecnicas/forms_tester/test_pf_list_words.html"
            response = self.getFirstPhase(request)
        elif rep == 2:
            response = self.getSecondPhase(request)
        elif rep >= 3:
            response = self.getRepetitionPhase(request)
        else:
            response = self.getErrorRepetition(request)

        return response

    def getFirstPhase(self, request: HttpRequest):
        self.participation.refresh_from_db()

        if self.participation.finalizado:
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse(self.previus_directory, kwargs=params))

        self.context["form"] = ListWordsForm()
        self.context["initial_phase"] = True

        return render(request, self.current_directory, self.context)

    def getSecondPhase(self, request: HttpRequest):
        self.participation.refresh_from_db()

        if self.participation.finalizado:
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse(self.previus_directory, kwargs=params))

        list_words = list(
            ListaPalabras.objects.get(
                tecnica=self.session.tecnica,
                catador=request.user.user_catador,
                es_final=False
            ).palabras.all()
        )

        self.context["form"] = ListWordsForm()
        self.context["initial_phase"] = False
        self.context["words"] = list_words

        return render(request, self.current_directory, self.context)

    def getRepetitionPhase(self, request: HttpRequest):
        technique = self.session.tecnica

        products_in_technique = Producto.objects.filter(id_tecnica=technique)

        words = list(
            ListaPalabras.objects.get(
                tecnica=self.session.tecnica,
                catador=request.user.user_catador,
                es_final=True
            ).palabras.all()
        )

        use_product: Producto = None
        use_words: list[Palabra] = None

        # Revisamos el producto que le falten calificaciones
        for current_product in products_in_technique:
            try:
                rating = Calificacion.objects.get(
                    num_repeticion=technique.repeticion,
                    id_producto=current_product,
                    id_tecnica=technique,
                    id_catador=self.tester
                )
            except Calificacion.DoesNotExist:
                # Si no hay calificacion mandamos el producto actual y todas la palabras
                use_product = current_product
                use_words = words
                break

            # Obtener los datos asociados para la calificacion para ver que palabras quedan por calificar
            recoreded_data = rating.dato_calificacion.all()

            if not recoreded_data:
                # Si no hay datos entonces devolver el producto con todas las palabras
                use_product = current_product
                use_words = words
                break
            else:
                words_to_use = PalabrasController.getWordsWithoutData(
                    recoreded_data=recoreded_data, words=words)

                # Si quedan palabras por calificar mandar las palabras con el producto
                if not isinstance(words_to_use, dict) and words_to_use:
                    use_product = current_product
                    use_words = words_to_use
                    break

        # Si no hay producto que falta por calificar finalizar sesion para el Catador
        if not use_product:
            updated_participation = ParticipacionController.finishSession(
                self.participation)
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse(self.previus_directory, kwargs=params))

        self.context["product"] = use_product
        self.context["words"] = use_words

        return render(request, self.current_directory, self.context)

    def getErrorRepetition(self, request: HttpRequest):
        params = {
            "code_sesion": self.session.codigo_sesion
        }
        return redirect(reverse(self.previus_directory, kwargs=params))
