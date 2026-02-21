from django.shortcuts import render
from django.http import HttpRequest
from tecnicas.models import Vocabulario


class ViewVocabularyController():
    context = {}
    current_url = "tecnicas/manage_vocabulary/view-vocabulary.html"

    def __init__(self):
        self.context = {}

    def controllGet(self, request: HttpRequest, nombre_vocabulario: str):
        try:
            vocabulary = Vocabulario.objects.get(
                nombre_vocabulario=nombre_vocabulario)
            
            self.context = {
                "vocabulary": vocabulary,
                "words": vocabulary.palabras.all().order_by('nombre_palabra')
            }
            
        except Vocabulario.DoesNotExist:
            self.context = {
                "error": f"No existe un vocabulario con el nombre '{nombre_vocabulario}'"
            }

        return render(request, self.current_url, self.context)
