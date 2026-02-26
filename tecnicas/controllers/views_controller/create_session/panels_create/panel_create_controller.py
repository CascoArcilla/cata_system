from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse


class PanelCreateController():
    def __init__(
            self,
            url_main: str = "cata_system:index",
            url_details: str = "cata_system:detalles_sesion"
    ):
        self.url_main = url_main
        self.url_details = url_details
        self.url_template = 'tecnicas/create_sesion/creating_session.html'

    def controllGet(self, request: HttpRequest):
        if request.session.get("technique_selected") == "general":
            self.url_main = "cata_system:index"

        context = {
            "url_main": reverse(self.url_main)
        }

        return render(request, self.url_template, context)

    def controllPost(self, request: HttpRequest):
        return JsonResponse({"message": "Creación con la técnica seleccionada no implementada"})
