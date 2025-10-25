from tecnicas.forms import SesionBasicForm
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse


class PanelBasicController():
    def __init__(self):
        pass

    @staticmethod
    def controllGetEscalas(request: HttpRequest):
        form_sesion = SesionBasicForm()
        response = render(
            request, "tecnicas/create_sesion/configuracion-panel-basic.html", {"form_sesion": form_sesion})
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
