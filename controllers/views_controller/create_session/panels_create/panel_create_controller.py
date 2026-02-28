from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse


class PanelCreateController():
    def __init__(
            self,
            url_home: str = "cata_system:index",
            url_details: str = "cata_system:detalles_sesion"
    ):
        self.url_home = url_home
        self.url_details = url_details
        self.url_template = 'create_sesion/creating_session.html'

    def controllGet(self, request: HttpRequest):
        if request.session.get("technique_selected") == "general":
            self.url_home = "cata_system:index"

        context = {
            "url_home": reverse(self.url_home)
        }

        return render(request, self.url_template, context)

    def controllPost(self, request: HttpRequest):
        return JsonResponse({"message": "Creación con la técnica seleccionada no implementada"})
