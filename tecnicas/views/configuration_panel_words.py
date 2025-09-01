from django.http import HttpRequest
from django.shortcuts import render
from ..models.palabra import Palabra
from ..forms.word_form import WordForm


def configurationPanelWords(req: HttpRequest):
    if req.method == "GET":
        form = WordForm()
        all_words = Palabra.objects.all()
        context = {
            "words": all_words,
            "form_word": form
        }
        return render(req, "tecnicas/create_sesion/configuracion-panel-words.html", context)
