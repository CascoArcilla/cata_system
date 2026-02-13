from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.forms import CodesForm
from tecnicas.utils import generarCodigos
import json


class PanelCodesController():
    url_current_panel = "tecnicas/create_sesion/conf-panel-codes.html"
    url_words = "cata_system:panel_configuracion_words"
    url_create_session = "cata_system:creando_sesion"

    def __init__(self):
        pass

    @staticmethod
    def controllGetEscalas(request: HttpRequest, data):
        """
        Obtain codes for scales technique
        Include orders for Catadores
        """
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
        """
        Post codes for scales technique
        Save orders for Catadores
        """
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
    def controllGetWithoutOrders(request: HttpRequest, data, name_technique: str):
        """
        Obtain codes for techniques without orders for Catadores
        """
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
    def controllPostNoOrdersWithWords(request: HttpRequest, name_technique: str):
        """
        Post codes for techniques without orders for Catadores
        Save codes and redirect to words panel or vocabulary panel
        """
        codes = []
        context_codes_form = {}

        for name, value in request.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(request.POST, codes=codes)

        context_codes_form = {
            "form_codes": form_codes,
            "use_technique": name_technique
        }

        if form_codes.is_valid():
            # Extract codes from cleaned_data to ensure uppercase conversion
            cleaned_codes = [value for name, value in form_codes.cleaned_data.items() if name.startswith('producto_')]
            request.session["form_codes"] = cleaned_codes
            return redirect(reverse(PanelCodesController.url_words))
        else:
            context_codes_form["error"] = "error en los datos recibidos"

        return render(request, PanelCodesController.url_current_panel, context_codes_form)

    @staticmethod
    def controllPostNoOrdersNoWords(request: HttpRequest, name_technique: str):
        """
        Post codes for techniques without orders for Catadores
        Save codes and redirect to create session panel
        For techniqes without style words
        """
        codes = []
        context_codes_form = {}

        for name, value in request.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(request.POST, codes=codes)

        context_codes_form = {
            "form_codes": form_codes,
            "use_technique": name_technique
        }

        if form_codes.is_valid():
            # Extract codes from cleaned_data to ensure uppercase conversion
            cleaned_codes = [value for name, value in form_codes.cleaned_data.items() if name.startswith('producto_')]
            request.session["form_codes"] = cleaned_codes
            return redirect(reverse(PanelCodesController.url_create_session))
        else:
            context_codes_form["error"] = "error en los datos recibidos"

        return render(request, PanelCodesController.url_current_panel, context_codes_form)
