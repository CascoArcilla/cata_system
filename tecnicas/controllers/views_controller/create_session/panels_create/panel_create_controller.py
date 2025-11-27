from django.http import JsonResponse, HttpRequest
from django.shortcuts import render

class PanelCreateController():
    url_template = 'tecnicas/create_sesion/creating_session.html'

    def __init__(self):
        pass

    @staticmethod
    def controllGet(request: HttpRequest):
        return render(
            request, PanelCreateController.url_template)

    @staticmethod
    def controllPost(request: HttpRequest):
        return JsonResponse({"message": "Método no permitido"})
