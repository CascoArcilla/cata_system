from django.http import HttpRequest
from tecnicas.forms import WordForm, VocabularioSelectForm
from django.shortcuts import render, redirect
from django.urls import reverse
from tecnicas.models import Palabra
import json


class PanelWordsController():
    def __init__(self, url_main: str = "cata_system:seleccion_tecnica"):
        self.template_atributes = "tecnicas/create_sesion/conf-panel-words.html"
        self.template_vocabulary = "tecnicas/create_sesion/conf-panel-vocabulary.html"
        self.context = {
            "url_main": reverse(url_main)
        }

    def controllGetAtributes(self, request: HttpRequest):
        """
        Form for words
        For techniques with style words "atributos"
        """
        form = WordForm()
        self.context["form_word"] = form

        if request.session.get("technique_selected") == "general":
            self.context["url_main"] = reverse("cata_system:seleccion_tecnica")

        return render(request, self.template_atributes, self.context)

    def controllGetVocabulary(self, request: HttpRequest):
        """
        Form for vocabulary
        For techniques with style words "vocabulario"
        """
        form = VocabularioSelectForm()
        self.context["form"] = form

        if request.session.get("technique_selected") == "general":
            self.context["url_main"] = reverse("cata_system:seleccion_tecnica")

        return render(request, self.template_vocabulary, self.context)

    def controllPostAtributes(self, request: HttpRequest):
        """
        Validate words
        For techniques with style words "atributos"
        """
        form = WordForm()
        self.context["form_word"] = form

        if request.session.get("technique_selected") == "general":
            self.context["url_main"] = reverse("cata_system:seleccion_tecnica")

        if not request.POST.get("words"):
            return render(request, self.template_atributes, self.context)

        words = json.loads(request.POST.get("words"))
        self.context["words"] = words

        ids_words = [word["id"] for word in words]

        if len(ids_words) != len(set(ids_words)):
            self.context["error"] = "existen palabras duplicadas"
            return render(request, self.template_atributes, self.context)

        exist_words = Palabra.objects.filter(
            id__in=ids_words).count() == len(ids_words)

        if not exist_words:
            self.context["error"] = "algunas palabras no existen"
            return render(request, self.template_atributes, self.context)

        request.session["form_words"] = ids_words
        return redirect(reverse("cata_system:creando_sesion"))

    def controllPostVocabulary(self, request: HttpRequest):
        """
        Validate vocabulary
        For techniques with style words "vocabulario"
        """
        if not request.POST.get("vocabulario"):
            self.context["form"] = VocabularioSelectForm()
            self.context["error"] = "No hay un vocabulario seleccionado"
            return render(request, self.template_vocabulary, self.context)

        form = VocabularioSelectForm(request.POST)
        vocabulary: int

        if request.session.get("technique_selected") == "general":
            self.context["url_main"] = reverse("cata_system:seleccion_tecnica")

        if form.is_valid():
            vocabulary = form.cleaned_data["vocabulario"]

        else:
            self.context["form"] = VocabularioSelectForm()
            self.context["error"] = "Erro al validar el vocabulario"
            return render(request, self.template_vocabulary, self.context)

        request.session["form_words"] = vocabulary.nombre_vocabulario
        return redirect(reverse("cata_system:creando_sesion"))
