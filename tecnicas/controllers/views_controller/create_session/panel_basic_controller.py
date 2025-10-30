from tecnicas.forms import SesionBasicForm
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse


class PanelBasicController():
    conf_initial_rata = {
        "numero_catadores": 0,
        "numero_repeticiones": 1
    }

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
            request, "tecnicas/create_sesion/configuracion-panel-basic.html", view_context)
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
                response = render(request, "tecnicas/create_sesion/configuracion-panel-basic.html", {
                    "form_sesion": form, "error": "Información no valida"})
        except KeyError:
            response = redirect(reverse(
                "cata_system:seleccion_tecnica") + "?error=error en datos de configuracion")

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
            request, "tecnicas/create_sesion/configuracion-panel-basic.html", view_context)
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
                    response = render(request, "tecnicas/create_sesion/configuracion-panel-basic.html", {
                        "form_sesion": form, "error": "No puedes modificar el número de catadores o repeticiones"})
                else:
                    values["name_tecnica"] = name_tecnica
                    request.session['form_basic'] = values
                    response = redirect(
                        reverse("cata_system:panel_configuracion_tags"))
            else:
                response = render(request, "tecnicas/create_sesion/configuracion-panel-basic.html", {
                    "form_sesion": form, "error": "Información no valida"})
        except KeyError:
            response = redirect(reverse(
                "cata_system:seleccion_tecnica") + "?error=error en datos de configuracion")

        return response
