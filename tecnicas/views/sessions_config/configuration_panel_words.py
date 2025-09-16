from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from ...models.palabra import Palabra
from ...forms import WordForm

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

        ids_words = [word["id"] for word in words]

        if len(ids_words) != len(set(ids_words)):
            context["error"] = "existen palabras duplicadas"
            return render(req, "tecnicas/create_sesion/configuracion-panel-words.html", context)

        exist_words = Palabra.objects.filter(
            id__in=ids_words).count() == len(ids_words)

        if not exist_words:
            context["error"] = "algunas palabras no existen"
            return render(req, "tecnicas/create_sesion/configuracion-panel-words.html", context)

        req.session["form_words"] = ids_words
        return redirect(reverse("cata_system:creando_sesion"))
