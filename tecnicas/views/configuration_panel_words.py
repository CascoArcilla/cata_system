from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from ..models.palabra import Palabra
from ..forms.word_form import WordForm

import json


def configurationPanelWords(req: HttpRequest):
    if not req.session.get("form_basic") or not req.session.get("form_tags") or not req.session.get("form_codes"):
        req.session.flush()
        return redirect(reverse("cata_system:seleccion_tecnica") +
                        "?error=datos del formulario requerido no encontrados")

    form = WordForm()
    context = {
        "form_word": form
    }

    if req.method == "GET":
        return render(req, "tecnicas/create_sesion/configuracion-panel-words.html", context)
    elif req.method == "POST":
        if not req.POST.get("words"):
            return render(req, "tecnicas/create_sesion/configuracion-panel-words.html", context)

        words = json.loads(req.POST.get("words"))

        context["words"] = words

        print(words)

        # form = WordForm(req.POST)
        # all_words = Palabra.objects.all()
        # context = {
        #     "words": all_words,
        #     "form_word": form
        # }

        # if form.is_valid():
        #     new_word = form.cleaned_data.get("nombre_palabra")
        #     if not Palabra.objects.filter(nombre_palabra__iexact=new_word).exists():
        #         Palabra.objects.create(nombre_palabra=new_word)
        #         context["form_word"] = WordForm()
        #         context["words"] = Palabra.objects.all()
        #     else:
        #         context["error"] = "La palabra ya existe"
        # else:
        #     context["error"] = "Error en los datos recibidos"

        return render(req, "tecnicas/create_sesion/configuracion-panel-words.html", context)
