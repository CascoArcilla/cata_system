from django.http import HttpRequest
from tecnicas.forms import WordForm, VocabularioSelectForm
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Palabra
import json


class PanelWordsController():
    def __init__(self, url_main: str = "cata_system:seleccion_tecnica", url_home: str = "cata_system:index"):
        self.template_atributes = "create_sesion/conf-panel-words.html"
        self.template_vocabulary = "create_sesion/conf-panel-vocabulary.html"
        self.url_main = url_main
        self.url_home = url_home

    def getContext(self, request: HttpRequest):
        if request.session.get("technique_selected") == "general":
            self.url_main = "cata_system:seleccion_tecnica"
            self.url_home = "cata_system:index"

        context = {
            "url_main": reverse(self.url_main),
            "home_url": reverse(self.url_home)
        }

        return context

    def controllGetAtributes(self, request: HttpRequest):
        """
        Form for words
        For techniques with style words "atributos"
        """
        form = WordForm()
        context = self.getContext(request)
        context["form_word"] = form

        return render(request, self.template_atributes, context)

    def controllGetVocabulary(self, request: HttpRequest):
        """
        Form for vocabulary
        For techniques with style words "vocabulario"
        """
        form = VocabularioSelectForm()
        context = self.getContext(request)
        context["form"] = form

        return render(request, self.template_vocabulary, context)

    def controllPostAtributes(self, request: HttpRequest):
        """
        Validate words
        For techniques with style words "atributos"
        """
        form = WordForm()
        context = self.getContext(request)
        context["form_word"] = form

        if not request.POST.get("words"):
            return render(request, self.template_atributes, context)

        words = json.loads(request.POST.get("words"))
        context["words"] = words

        ids_words = [word["id"] for word in words]

        if len(ids_words) != len(set(ids_words)):
            context["error"] = "existen palabras duplicadas"
            return render(request, self.template_atributes, context)

        exist_words = Palabra.objects.filter(
            id__in=ids_words).count() == len(ids_words)

        if not exist_words:
            context["error"] = "algunas palabras no existen"
            return render(request, self.template_atributes, context)

        request.session["form_words"] = ids_words
        return redirect(reverse("cata_system:creando_sesion"))

    def controllPostVocabulary(self, request: HttpRequest):
        """
        Validate vocabulary
        For techniques with style words "vocabulario"
        """
        context = self.getContext(request)

        if not request.POST.get("vocabulario"):
            context["form"] = VocabularioSelectForm()
            context["error"] = "No hay un vocabulario seleccionado"
            return render(request, self.template_vocabulary, context)

        form = VocabularioSelectForm(request.POST)
        vocabulary: int

        if form.is_valid():
            vocabulary = form.cleaned_data["vocabulario"]

        else:
            context["form"] = VocabularioSelectForm()
            context["error"] = "Erro al validar el vocabulario"
            return render(request, self.template_vocabulary, context)

        request.session["form_words"] = vocabulary.nombre_vocabulario
        return redirect(reverse("cata_system:creando_sesion"))
