from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.forms import CodesForm
from tecnicas.utils import generarCodigos
import json


class PanelCodesController():
    url_current_panel = "tecnicas/create_sesion/configuracion-panel-codes.html"
    url_words = "cata_system:panel_configuracion_words"
    url_create_session = "cata_system:creando_sesion"

    def __init__(self):
        pass

    @staticmethod
    def controllGetEscalas(request: HttpRequest, data):
        num_products = data["numero_productos"]
        num_tester = data["numero_catadores"]

        codes_products = generarCodigos(num_products)

        form_codes = CodesForm(codes=codes_products)

        context_codes_form = {
            "form_codes": form_codes,
            "num_tester": num_tester,
            "use_technique": "escalas"
        }

        return render(request, PanelCodesController.url_current_panel, context_codes_form)

    @staticmethod
    def controllPostEscalas(request: HttpRequest, data):
        num_tester = data["numero_catadores"]

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
            "use_technique": "escalas"
        }

        if form_codes.is_valid():
            codes_sort = {"product_codes": []}

            for name, value in form_codes.cleaned_data.items():
                codes_sort["product_codes"].append({name: value})

            codes_sort["sort_codes"] = sorts_code
            request.session["form_codes"] = codes_sort
            return redirect(reverse(PanelCodesController.url_words))
        else:
            context_codes_form["error"] = "error en los datos recibidos"

        return render(request, PanelCodesController.url_current_panel, context_codes_form)

    @staticmethod
    def controllGetRATA(request: HttpRequest, data, name_technique: str):
        num_products = data["numero_productos"]
        codes_products = generarCodigos(num_products)
        form_codes = CodesForm(codes=codes_products)

        context_codes_form = {
            "form_codes": form_codes,
            "num_tester": 0,
            "use_technique": name_technique
        }

        return render(request, PanelCodesController.url_current_panel, context_codes_form)

    @staticmethod
    def controllPostRATA(request: HttpRequest, is_rata: True):
        codes = []
        context_codes_form = {}

        for name, value in request.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(request.POST, codes=codes)

        context_codes_form = {
            "form_codes": form_codes,
            "use_technique": "rata" if is_rata else "cata"
        }

        if form_codes.is_valid():
            request.session["form_codes"] = codes
            return redirect(reverse(PanelCodesController.url_words))
        else:
            context_codes_form["error"] = "error en los datos recibidos"

        return render(request, PanelCodesController.url_current_panel, context_codes_form)

    @staticmethod
    def controllGetCATA(request: HttpRequest, data):
        num_products = data["numero_productos"]
        codes_products = generarCodigos(num_products)
        form_codes = CodesForm(codes=codes_products)

        context_codes_form = {
            "form_codes": form_codes,
            "use_technique": "cata"
        }

        return render(request, PanelCodesController.url_current_panel, context_codes_form)

    @staticmethod
    def controllPostPF(request: HttpRequest):
        codes = []
        context_codes_form = {}

        for name, value in request.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(request.POST, codes=codes)

        context_codes_form = {
            "form_codes": form_codes,
            "use_technique": "perfil flash"
        }

        if form_codes.is_valid():
            request.session["form_codes"] = codes
            return redirect(reverse(PanelCodesController.url_create_session))
        else:
            context_codes_form["error"] = "error en los datos recibidos"

        return render(request, PanelCodesController.url_current_panel, context_codes_form)
