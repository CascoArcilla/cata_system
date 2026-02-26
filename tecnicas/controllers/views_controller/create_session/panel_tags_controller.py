from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.forms import SesionTagsForm, EtiquetaForm
from tecnicas.models import TipoEscala


class PanelTagsController():
    def __init__(self, technique_name: str, url_main: str = "cata_system:seleccion_tecnica"):
        self.template = "tecnicas/create_sesion/conf-panel-tags.html"
        self.technique_name = technique_name
        self.url_main = url_main

    def controllGetEscalas(self, request: HttpRequest, data):
        (
            type_scale,
            tamano_escala,
            form_new_etiqueta
        ) = self.defineInfoScale(data)

        form_etiqutas = SesionTagsForm(
            longitud=tamano_escala, tipo_escala=type_scale.nombre_escala)

        if request.session.get("technique_selected") == "general":
            self.url_main = "cata_system:seleccion_tecnica"

        context_tags = {
            "form_tags": form_etiqutas,
            "form_new_tag": form_new_etiqueta,
            "use_technique": self.technique_name,
            "url_main": reverse(self.url_main),
        }

        return render(request, self.template, context_tags)

    def controllPostEscalas(self, request: HttpRequest, data):
        (
            type_scale,
            tamano_escala,
            form_new_etiqueta
        ) = self.defineInfoScale(data)

        values = {}
        form = SesionTagsForm(
            request.POST, longitud=tamano_escala,
            tipo_escala=type_scale.nombre_escala
        )

        if request.session.get("technique_selected") == "general":
            self.url_main = "cata_system:seleccion_tecnica"

        if form.is_valid():
            for name, value in form.cleaned_data.items():
                values[name] = value.id

            request.session["form_tags"] = values
            response = redirect(
                reverse("cata_system:panel_configuracion_codes"))
        else:
            context_tags = {
                "form_tags": form,
                "form_new_tag": form_new_etiqueta,
                "use_technique": self.technique_name,
                "url_main": reverse(self.url_main),
            }

            context_tags["error"] = "ha ocurrido un error"
            response = render(
                request, self.template, context_tags)

        return response

    def defineInfoScale(self, data):
        type_scale = TipoEscala.objects.get(pk=data["tipo_escala"])
        tamano_escala = data["tamano_escala"]
        form_new_etiqueta = EtiquetaForm()

        return (
            type_scale,
            tamano_escala,
            form_new_etiqueta
        )
