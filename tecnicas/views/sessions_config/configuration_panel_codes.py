from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from ...utils import generarCodigos
from ...forms import CodesForm
import json


def configurationPanelCodes(req: HttpRequest):
    if not req.session.get("form_basic") or not req.session.get("form_tags"):
        req.session.flush()
        return redirect(reverse("cata_system:seleccion_tecnica") +
                        "?error=datos del formulario requerido no encontrados")

    data_basic = req.session["form_basic"]

    num_products = data_basic["numero_productos"]
    num_tester = data_basic["numero_catadores"]

    if req.method == "GET":
        codes_products = generarCodigos(num_products)

        form_codes = CodesForm(codes=codes_products)

        context_codes_form = {
            "form_codes": form_codes,
            "num_tester": num_tester
        }

        return render(req, "tecnicas/create_sesion/configuracion-panel-codes.html", context_codes_form)
    elif req.method == "POST":
        sorts_code = json.loads(req.POST.get("sort_codes"))
        codes = []
        context_codes_form = {}

        for name, value in req.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(req.POST, codes=codes)

        context_codes_form = {
            "form_codes": form_codes,
            "num_tester": num_tester,
        }

        if form_codes.is_valid():
            codes_sort = {"product_codes": []}

            for name, value in form_codes.cleaned_data.items():
                codes_sort["product_codes"].append({name: value})

            codes_sort["sort_codes"] = sorts_code
            req.session["form_codes"] = codes_sort
            return redirect(reverse("cata_system:panel_configuracion_words"))
        else:
            context_codes_form["error"] = "error en los datos recibidos"

        return render(req, "tecnicas/create_sesion/configuracion-panel-codes.html", context_codes_form)
