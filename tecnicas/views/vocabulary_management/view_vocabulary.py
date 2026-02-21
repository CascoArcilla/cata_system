from django.shortcuts import render
from django.http import HttpRequest
from controllers import ViewVocabularyController


def viewVocabulary(req: HttpRequest, nombre_vocabulario: str):
    view_controller = ViewVocabularyController()
    if req.method == "GET":
        response = view_controller.controllGet(req, nombre_vocabulario)
        return response
    else:
        context = {"error": "Método no permitido"}
        return render(req, "tecnicas/manage_vocabulary/view-vocabulary.html", context)
