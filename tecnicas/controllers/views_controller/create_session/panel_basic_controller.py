from tecnicas.forms import SesionBasicForm, SesionBasicCATAForm
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse


class PanelBasicController():
    conf_initial_rata = {
        "numero_catadores": 0,
        "numero_repeticiones": 1
    }

    url_panel_basic = "tecnicas/create_sesion/configuracion-panel-basic.html"
    url_panel_basic_cata = "tecnicas/create_sesion/panel-basic-cata.html"

    url_next_panel_scales = "cata_system:panel_configuracion_tags"
    url_next_panel_cata = "cata_system:panel_configuracion_tags"

    url_select_technique = "cata_system:seleccion_tecnica"

    def __init__(self):
        pass

    @staticmethod
    def controllGetEscalas(request: HttpRequest):
        form_sesion = SesionBasicForm()

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": "escalas"
        }

        response = render(
            request, PanelBasicController.url_panel_basic, view_context)
        return response

    @staticmethod
    def controllPostEscalas(request: HttpRequest, name_tecnica: str):
        try:
            form = SesionBasicForm(request.POST)

            if form.is_valid():
                values = {}
                for name, value in form.cleaned_data.items():
                    if name == "estilo_palabras" or name == "tipo_escala":
                        values[name] = value.id
                    else:
                        values[name] = value

                values["name_tecnica"] = name_tecnica
                request.session['form_basic'] = values
                response = redirect(
                    reverse("cata_system:panel_configuracion_tags"))
            else:
                response = render(request, PanelBasicController.url_panel_basic, {
                    "form_sesion": form, "error": "Información no valida"})
        except KeyError:
            response = redirect(reverse(
                PanelBasicController.url_select_technique) + "?error=error en datos de configuracion")

        return response

    @staticmethod
    def controllGetRATA(request: HttpRequest):
        form_sesion = SesionBasicForm(
            initial_conf=PanelBasicController.conf_initial_rata)

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": "rata"
        }

        response = render(
            request, PanelBasicController.url_panel_basic, view_context)
        return response

    @staticmethod
    def controllPostRATA(request: HttpRequest, name_tecnica: str):
        try:
            form = SesionBasicForm(
                request.POST, initial_conf=PanelBasicController.conf_initial_rata)

            if form.is_valid():
                values = {}
                for name, value in form.cleaned_data.items():
                    if name == "estilo_palabras" or name == "tipo_escala":
                        values[name] = value.id
                    else:
                        values[name] = value

                for key, expected in PanelBasicController.conf_initial_rata.items():
                    actual = values.get(key)

                    if actual is None or str(actual) != str(expected):
                        form.add_error(
                            key, f"Valor inválido para '{key}': se esperaba {expected}, se recibió {actual}")

                if form.errors:
                    response = render(request, PanelBasicController.url_panel_basic, {
                        "form_sesion": form, "error": "No puedes modificar el número de catadores o repeticiones"})
                else:
                    values["name_tecnica"] = name_tecnica
                    request.session['form_basic'] = values
                    response = redirect(
                        reverse("cata_system:panel_configuracion_tags"))
            else:
                response = render(request, PanelBasicController.url_panel_basic, {
                    "form_sesion": form, "error": "Información no valida"})
        except KeyError:
            response = redirect(reverse(
                PanelBasicController.url_select_technique) + "?error=error en datos de configuracion")

        return response

    @staticmethod
    def controllGetCATA(request: HttpRequest):
        form_sesion = SesionBasicCATAForm()

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": "cata"
        }

        return render(
            request, PanelBasicController.url_panel_basic_cata, view_context)

    @staticmethod
    def controllPostRATA(request: HttpRequest, name_tecnica: str):
        form = SesionBasicCATAForm(request.POST)

        if form.is_valid():
            values = {}
            for name, value in form.cleaned_data.items():
                if name == "estilo_palabras":
                    values[name] = value.id
                else:
                    values[name] = value

            values["name_tecnica"] = name_tecnica
            request.session['form_basic'] = values
            response = redirect(
                reverse(PanelBasicController.url_next_panel_cata))
        else:
            response = render(request, PanelBasicController.url_panel_basic, {
                "form_sesion": form, "error": "Información no valida"})

        return response
