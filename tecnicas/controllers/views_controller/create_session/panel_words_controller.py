from django.http import HttpRequest
from tecnicas.forms import WordForm
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Palabra
import json


class PanelWordsController():
    def __init__(self):
        pass

    @staticmethod
    def controllGetEscalas(request: HttpRequest):
        form = WordForm()
        context = {
            "form_word": form
        }

        return render(request, "tecnicas/create_sesion/configuracion-panel-words.html", context)

    @staticmethod
    def controllPostEscalas(request: HttpRequest):
        form = WordForm()
        context = {
            "form_word": form
        }

        if not request.POST.get("words"):
            return render(request, "tecnicas/create_sesion/configuracion-panel-words.html", context)

        words = json.loads(request.POST.get("words"))
        context["words"] = words

        ids_words = [word["id"] for word in words]

        if len(ids_words) != len(set(ids_words)):
            context["error"] = "existen palabras duplicadas"
            return render(request, "tecnicas/create_sesion/configuracion-panel-words.html", context)

        exist_words = Palabra.objects.filter(
            id__in=ids_words).count() == len(ids_words)

        if not exist_words:
            context["error"] = "algunas palabras no existen"
            return render(request, "tecnicas/create_sesion/configuracion-panel-words.html", context)

        request.session["form_words"] = ids_words
        return redirect(reverse("cata_system:creando_sesion"))
