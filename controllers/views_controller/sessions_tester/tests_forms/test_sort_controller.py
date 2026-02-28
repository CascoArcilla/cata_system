from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.models import Participacion, Producto, Calificacion, Palabra, GrupoProducto
from controllers import ParticipacionController, PalabrasController, EscalaController
from tecnicas.forms import ListWordsForm
from .general_test_controller import GenetalTestController


class TestSortController(GenetalTestController):
    def __init__(self, sensorial_session, user_tester):
        super().__init__(sensorial_session, user_tester)
        self.current_directory = "forms_tester/test_sort.html"

    def controllGet(self, request: HttpRequest):
        '''
        Objetivo: Entregar al cliente los grupos de productos guardados hechos por el catador en una lista, de lo contrario solo mandar una lista vacia
        - Comprobar que el Catador aun no finalice su la sesion
        - Obtener todos los productos en la tecnica
        - Obtener todos los grupos creadas por el usuario
            - Si hay grupos, cada item de la lista a mandar debe incluir los productos asociados al grupo como las palabras que describen al grupo
            - Si no hay grupos, solo mandar una lista vacia
        - Mandar la lista de grupos como la lista de productos
        - Agregar el formulario para describir los grupo
        '''
        self.context["session"] = self.session
        technique = self.session.tecnica

        self.participation = Participacion.objects.get(
            tecnica=technique, catador=request.user.user_catador)

        # Comprobar que el Catador no haya finalizado
        if self.participation.finalizado:
            params = {
                "code_sesion": self.session.codigo_sesion
            }
            return redirect(reverse(self.previus_directory, kwargs=params))

        products_in_technique = Producto.objects.filter(id_tecnica=technique)
        self.context["products"] = products_in_technique

        grups_products = GrupoProducto.objects.filter(
            tecnica=technique, catador=request.user.user_catador)

        self.context["grups_products"] = grups_products or []

        self.context["form_word"] = ListWordsForm()

        return render(request, self.current_directory, self.context)
