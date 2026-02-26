from tecnicas.forms import SesionBasicForm, SesionBasicCATAForm, SesionBasicPFForm, SesionBasicSortForm, SesionBasicNappingForm, SesionBasicRATAForm, SesionBasicIdealForm
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse


class PanelBasicController():
    conf_initial_rata = {
        "numero_catadores": 0,
        "numero_repeticiones": 1
    }

    def __init__(self):
        self.template = "tecnicas/create_sesion/conf-panel-basic.html"
        self.url_conf_tags = "cata_system:panel_configuracion_tags"
        self.url_conf_codes = "cata_system:panel_configuracion_codes"
        self.url_main = "cata_system:seleccion_tecnica"
        self.default_url_main = "cata_system:seleccion_tecnica"

    def controllGetEscalas(self, request: HttpRequest):
        form_sesion = SesionBasicForm()

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": "escalas",
            "url_main":  reverse(self.default_url_main) if request.session.get("technique_selected") != "escalas" else reverse("cata_system:index_escalas")
        }

        response = render(
            request, self.template, view_context)
        return response

    def controllPostEscalas(self, request: HttpRequest, name_tecnica: str):
        try:
            form = SesionBasicForm(request.POST)

            if form.is_valid():
                values = {}
                for name, value in form.cleaned_data.items():
                    if name == "tipo_escala":
                        values[name] = value.id
                    else:
                        values[name] = value

                values["name_tecnica"] = name_tecnica
                request.session['form_basic'] = values
                response = redirect(
                    reverse(self.url_conf_tags))
            else:
                response = render(request, self.template, {
                    "form_sesion": form,
                    "error": "Información no valida",
                    "use_technique": "escalas",
                    "url_main": reverse(self.default_url_main) if request.session.get("technique_selected") != "escalas" else reverse("cata_system:index_escalas")
                })
        except KeyError:
            url_main = reverse(self.default_url_main) if request.session.get("technique_selected") != "escalas" else reverse("cata_system:index_escalas")
            response = redirect(url_main + "?error=error en datos de configuracion")

        return response

    def controllGetRATA(self, request: HttpRequest):
        form_sesion = SesionBasicRATAForm()

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": "rata"
        }

        response = render(
            request, self.template, view_context)
        return response

    def controllPostRATA(self, request: HttpRequest, name_tecnica: str):
        try:
            form = SesionBasicRATAForm(request.POST)

            if form.is_valid():
                values = {}
                for name, value in form.cleaned_data.items():
                    if name == "tipo_escala":
                        values[name] = value.id
                    else:
                        values[name] = value

                if form.errors:
                    response = render(request, self.template, {
                        "form_sesion": form, "error": "No puedes modificar el número de catadores o repeticiones", "use_technique": "rata"})
                else:
                    values["name_tecnica"] = name_tecnica
                    request.session['form_basic'] = values
                    response = redirect(
                        reverse(self.url_conf_tags))
            else:
                response = render(request, self.template, {
                    "form_sesion": form, "error": "Información no valida", "use_technique": "rata"})
        except KeyError:
            response = redirect(reverse(
                self.url_main) + "?error=error en datos de configuracion")

        return response

    def controllGetCATA(self, request: HttpRequest):
        form_sesion = SesionBasicCATAForm()

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": "cata"
        }

        return render(
            request, self.template, view_context)

    def controllPostCATA(self, request: HttpRequest, name_tecnica: str):
        form = SesionBasicCATAForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(self.url_conf_codes))
        else:
            response = render(request, self.template, {
                "form_sesion": form, "error": "Información no valida", "use_technique": "cata"})

        return response

    def controllGetPF(self, request: HttpRequest):
        form_sesion = SesionBasicPFForm()

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": "perfil flash"
        }

        return render(
            request, self.template, view_context)

    def controllPostPF(self, request: HttpRequest, name_tecnica: str):
        form = SesionBasicPFForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(self.url_conf_codes))
        else:
            response = render(request, self.template, {
                "form_sesion": form, "error": "Información no valida", "use_technique": "perfil flash"})

        return response

    def controllGetSort(self, request: HttpRequest):
        form_sesion = SesionBasicSortForm()

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": "sort"
        }

        return render(
            request, self.template, view_context)

    def controllPostSort(self, request: HttpRequest, name_tecnica: str):
        form = SesionBasicSortForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(self.url_conf_codes))
        else:
            response = render(request, self.template, {
                "form_sesion": form, "error": "Información no valida", "use_technique": "sort"})

        return response

    def controllGetNapping(self, request: HttpRequest):
        form_sesion = SesionBasicNappingForm()

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": "napping"
        }

        return render(
            request, self.template, view_context)

    def controllPostNapping(self, request: HttpRequest, name_tecnica: str):
        form = SesionBasicNappingForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(self.url_conf_codes))
        else:
            response = render(request, self.template, {
                "form_sesion": form, "error": "Información no valida", "use_technique": "napping"})

        return response

    def controllGetIdeal(self, request: HttpRequest):
        form_sesion = SesionBasicIdealForm()

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": "perfil_ideal"
        }

        return render(
            request, self.template, view_context)

    def controllPostIdeal(self, request: HttpRequest, name_tecnica: str):
        form = SesionBasicIdealForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(self.url_conf_codes))
        else:
            response = render(request, self.template, {
                "form_sesion": form, "error": "Información no valida", "use_technique": "perfil_ideal"})

        return response
