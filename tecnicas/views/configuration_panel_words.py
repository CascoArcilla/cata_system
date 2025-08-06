from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from ..utils import generarCodigos
from ..forms import PalabrasForm
import json

def configurationsPanelWords(req:HttpRequest):
    data_basic = req.session["form_basic"]
    data_tags = req.session["form_tags"]

    if not data_basic or not data_tags:
        redirect(reverse("cata_system:seleccion_tecnica") + "?error=datos del formulario requerido no encontrados")

    num_products = data_basic["numero_productos"]
    num_cata = data_basic["numero_jueces"]

    if req.method == "GET":
        codes_products = generarCodigos(num_products)

        form_worlds = PalabrasForm(codes=codes_products)

        context_worlds_form = {
            "form_worlds" : form_worlds,
            "num_cata": num_cata
        }
        
        return render(req, "tecnicas/configuracion-panel-palabras.html", context_worlds_form)
    elif req.method == "POST":
        sorts_code = json.loads(req.POST.get("sort_codes"))
        codes = []

        for name, value in req.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_worlds = PalabrasForm(req.POST, codes=codes)

        if form_worlds.is_valid():
            code_sort = {"product_codes":[]}

            for name, value in form_worlds.cleaned_data.items():
                code_sort["product_codes"].append({name: value})

            code_sort["sort_codes"] = sorts_code

            print(code_sort)
            print("Todo ok")
        else:
            print("datos no validos")
        
        context_worlds_form = {
            "form_worlds" : form_worlds,
            "num_cata": num_cata,
            "error": "error en los datos recibidos"
        }

        return render(req, "tecnicas/configuracion-panel-palabras.html", context_worlds_form)