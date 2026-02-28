from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.forms import CodesForm
from utils import generarCodigos
import json


class PanelCodesController():
    def __init__(
        self,
        url_next: str = "cata_system:panel_configuracion_words",
        url_main: str = "cata_system:seleccion_tecnica",
        url_home: str = "cata_system:index"
    ):
        self.template = "tecnicas/create_sesion/conf-panel-codes.html"
        self.url_next = url_next
        self.url_main = url_main
        self.url_home = url_home

    def getContext(
        self, form_codes, use_technique,
        select_technique, num_tester: int = None
    ):
        if select_technique == "general":
            self.url_main = "cata_system:seleccion_tecnica"
            self.url_home = "cata_system:index"

        context = {
            "form_codes": form_codes,
            "use_technique": use_technique,
            "url_main": reverse(self.url_main),
            "home_url": reverse(self.url_home)
        }

        if num_tester:
            context["num_tester"] = num_tester

        return context

    def controllGetEscalas(self, request: HttpRequest, data):
        """
        Obtain codes for scales technique
        Include orders for Catadores
        """
        num_products = data["numero_productos"]
        num_tester = data["numero_catadores"]

        codes_products = generarCodigos(num_products)

        form_codes = CodesForm(codes=codes_products)

        context = self.getContext(
            form_codes=form_codes,
            use_technique="escalas",
            select_technique=request.session.get("technique_selected"),
            num_tester=num_tester
        )

        return render(request, self.template, context)

    def controllPostEscalas(self, request: HttpRequest, data):
        """
        Post codes for scales technique
        Save orders for Catadores
        """
        num_tester = data["numero_catadores"]

        sorts_code = json.loads(request.POST.get("sort_codes"))
        codes = []

        for name, value in request.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(request.POST, codes=codes)

        context = self.getContext(
            form_codes=form_codes,
            use_technique="escalas",
            select_technique=request.session.get("technique_selected"),
            num_tester=num_tester
        )

        if form_codes.is_valid():
            codes_sort = {"product_codes": []}

            for name, value in form_codes.cleaned_data.items():
                codes_sort["product_codes"].append({name: value})

            codes_sort["sort_codes"] = sorts_code
            request.session["form_codes"] = codes_sort
            return redirect(reverse(self.url_next))
        else:
            self.context["error"] = "error en los datos recibidos"

        return render(request, self.template, self.context)

    def controllGetNoOrders(self, request: HttpRequest, data, name_technique: str):
        """
        Obtain codes for techniques without orders for Catadores
        """
        num_products = data["numero_productos"]
        codes_products = generarCodigos(num_products)
        form_codes = CodesForm(codes=codes_products)

        conf_basic = "cata_system:panel_configuracion_basic"

        technique_without_tags = {
            "perfil-flash": "?name_tecnica=perfil flash",
            "sort": "?name_tecnica=sort",
            "napping": "?name_tecnica=napping",
            "perfil-ideal": "?name_tecnica=perfil_ideal",
            "cata": "?name_tecnica=cata"
        }

        technique_select = request.session.get("technique_selected")

        context = self.getContext(
            form_codes=form_codes,
            use_technique=name_technique,
            select_technique=technique_select
        )

        if technique_select in technique_without_tags:
            context["back_url"] = reverse(conf_basic) + technique_without_tags[technique_select]

        return render(request, self.template, context)

    def controllPostNoOrders(self, request: HttpRequest, name_technique: str):
        """
        Post codes for techniques without orders for Catadores
        Save codes and redirect to words panel or vocabulary panel
        """
        codes = []

        for name, value in request.POST.items():
            if name.__contains__("producto_"):
                codes.append(value)

        form_codes = CodesForm(request.POST, codes=codes)

        if form_codes.is_valid():
            # Extract codes from cleaned_data to ensure uppercase conversion
            cleaned_codes = [value for name, value in form_codes.cleaned_data.items(
            ) if name.startswith('producto_')]
            request.session["form_codes"] = cleaned_codes
            return redirect(reverse(self.url_next))

        else:
            context = self.getContext(
                form_codes=form_codes,
                use_technique=name_technique,
                select_technique=request.session.get("technique_selected")
            )
            context["error"] = "error en los datos recibidos"

        return render(request, self.template, context)
