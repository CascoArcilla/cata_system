from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse


class ConfBasicController():
    def __init__(self, template_name: str, next_url: str, form_class):
        self.template_name = template_name
        self.next_url = next_url
        self.form_class = form_class

    def get(self, request: HttpRequest, name_tecnica: str):
        form_sesion = self.form_class()

        view_context = {
            "form_sesion": form_sesion,
            "use_technique": name_tecnica
        }

        response = render(request, self.template_name, view_context)
        return response

    def post(self, request: HttpRequest, name_tecnica: str):
        try:
            form = self.form_class(request.POST)

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
                    reverse(self.next_url))
            else:
                response = render(request, self.template_name, {
                    "form_sesion": form,
                    "error": "Información no valida",
                    "use_technique": name_tecnica
                })
        except KeyError:
            response = redirect(reverse(
                PanelBasicController.url_select_technique) + "?error=error en datos de configuracion")

        return response
