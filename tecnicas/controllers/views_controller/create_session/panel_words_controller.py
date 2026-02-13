from django.http import HttpRequest
from tecnicas.forms import WordForm, VocabularioSelectForm
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Palabra
import json


class PanelWordsController():
    current_url_atribute = "tecnicas/create_sesion/conf-panel-words.html"
    current_url_vocabulary = "tecnicas/create_sesion/conf-panel-vocabulary.html"

    def __init__(self):
        pass

    @staticmethod
    def controllGetAtributes(request: HttpRequest):
        """
        Form for words
        For techniques with style words "atributos"
        """
        form = WordForm()
        context = {
            "form_word": form
        }

        return render(request, PanelWordsController.current_url_atribute, context)

    @staticmethod
    def controllGetVocabulary(request: HttpRequest):
        """
        Form for vocabulary
        For techniques with style words "vocabulario"
        """
        form = VocabularioSelectForm()
        context = {"form": form}
        return render(request, PanelWordsController.current_url_vocabulary, context)

    @staticmethod
    def controllPostAtributes(request: HttpRequest):
        """
        Validate words
        For techniques with style words "atributos"
        """
        form = WordForm()
        context = {
            "form_word": form
        }

        if not request.POST.get("words"):
            return render(request, PanelWordsController.current_url_atribute, context)

        words = json.loads(request.POST.get("words"))
        context["words"] = words

        ids_words = [word["id"] for word in words]

        if len(ids_words) != len(set(ids_words)):
            context["error"] = "existen palabras duplicadas"
            return render(request, PanelWordsController.current_url_atribute, context)

        exist_words = Palabra.objects.filter(
            id__in=ids_words).count() == len(ids_words)

        if not exist_words:
            context["error"] = "algunas palabras no existen"
            return render(request, PanelWordsController.current_url_atribute, context)

        request.session["form_words"] = ids_words
        return redirect(reverse("cata_system:creando_sesion"))

    @staticmethod
    def controllPostVocabulary(request: HttpRequest):
        """
        Validate vocabulary
        For techniques with style words "vocabulario"
        """
        context = {}
        if not request.POST.get("vocabulario"):
            context["form"] = VocabularioSelectForm()
            context["error"] = "No hay un vocabulario seleccionado"
            return render(request, PanelWordsController.current_url_vocabulary, context)

        form = VocabularioSelectForm(request.POST)
        vocabulary: int
        if form.is_valid():
            vocabulary = form.cleaned_data["vocabulario"]
        else:
            context["form"] = VocabularioSelectForm()
            context["error"] = "Erro al validar el vocabulario"
            return render(request, PanelWordsController.current_url_vocabulary, context)

        request.session["form_words"] = vocabulary.nombre_vocabulario
        return redirect(reverse("cata_system:creando_sesion"))
