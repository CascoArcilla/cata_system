from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.forms import CodesForm
from tecnicas.utils import generarCodigos
import json


class PanelCodesController():
    def __init__(self):
        pass

    @staticmethod
    def controllGetConvencional(request: HttpRequest, data):
        (
            num_products,
            num_tester
        ) = PanelCodesController.defineInfoConvencional(data)

        codes_products = generarCodigos(num_products)

        form_codes = CodesForm(codes=codes_products)

        context_codes_form = {
            "form_codes": form_codes,
            "num_tester": num_tester
        }

        return render(request, "tecnicas/create_sesion/configuracion-panel-codes.html", context_codes_form)

    @staticmethod
    def controllPostConvencional(request: HttpRequest, data):
        (
            num_products,
            num_tester
        ) = PanelCodesController.defineInfoConvencional(data)

        sorts_code = json.loads(request.POST.get("sort_codes"))
        codes = []
        context_codes_form = {}

        for name, value in request.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(request.POST, codes=codes)

        context_codes_form = {
            "form_codes": form_codes,
            "num_tester": num_tester,
        }

        if form_codes.is_valid():
            codes_sort = {"product_codes": []}

            for name, value in form_codes.cleaned_data.items():
                codes_sort["product_codes"].append({name: value})

            codes_sort["sort_codes"] = sorts_code
            request.session["form_codes"] = codes_sort
            return redirect(reverse("cata_system:panel_configuracion_words"))
        else:
            context_codes_form["error"] = "error en los datos recibidos"

        return render(request, "tecnicas/create_sesion/configuracion-panel-codes.html", context_codes_form)

    @staticmethod
    def defineInfoConvencional(data):
        num_products = data["numero_productos"]
        num_tester = data["numero_catadores"]
        return (
            num_products,
            num_tester
        )
