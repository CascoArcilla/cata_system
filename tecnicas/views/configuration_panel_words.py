from django.http import HttpRequest
from django.shortcuts import render
from ..models.palabra import Palabra

def configurationPanelWords(req: HttpRequest):
    if req.method == "GET":
        allWords =  Palabra.objects.all()
        context = {
            "words": allWords
        }
        return render(req, "tecnicas/create_sesion/configuracion-panel-words.html", context)