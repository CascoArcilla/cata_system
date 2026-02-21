from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.forms import CodesForm
from utils import generarCodigos
import json


class ConfCodesController():
    def __init__(self, template: str = "views/conf-panel-codes.html", next_url: str = "cata_system:panel_configuracion_words", data: dict = {}):
        self.template = template
        self.next_url = next_url
        self.data = data

    def getOrders(self, request: HttpRequest):
        """
        Obtain codes for scales technique
        Include orders for Catadores
        """
        num_products = self.data["numero_productos"]
        num_tester = self.data["numero_catadores"]

        codes_products = generarCodigos(num_products)

        form_codes = CodesForm(codes=codes_products)

        context_codes_form = {
            "form_codes": form_codes,
            "num_tester": num_tester,
            "use_technique": "escalas"
        }

        return render(request, self.template, context_codes_form)

    def postOrders(self, request: HttpRequest):
        """
        Post codes for scales technique
        Save orders for Catadores
        """
        num_tester = self.data["numero_catadores"]

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
            return redirect(reverse(self.next_url))
        else:
            context_codes_form["error"] = "error en los datos recibidos"

        return render(request, self.template, context_codes_form)

    def getNoOrders(self, request: HttpRequest, name_technique: str):
        """
        Obtain codes for techniques without orders for Catadores
        """
        num_products = self.data["numero_productos"]
        codes_products = generarCodigos(num_products)
        form_codes = CodesForm(codes=codes_products)

        context_codes_form = {
            "form_codes": form_codes,
            "num_tester": 0,
            "use_technique": name_technique
        }

        return render(request, self.template, context_codes_form)

    def postNoOrders(self, request: HttpRequest, name_technique: str):
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
            cleaned_codes = [value for name, value in form_codes.cleaned_data.items(
            ) if name.startswith('producto_')]
            request.session["form_codes"] = cleaned_codes
            return redirect(reverse(self.next_url))
        else:
            context_codes_form["error"] = "error en los datos recibidos"

        return render(request, self.template, context_codes_form)