from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.forms import SesionTagsForm, EtiquetaForm
from tecnicas.models import TipoEscala


class PanelTagsController():
    def __init__(self, technique_name: str, url_main: str = "cata_system:seleccion_tecnica", url_home: str = "cata_system:index"):
        self.template = "create_sesion/conf-panel-tags.html"
        self.technique_name = technique_name
        self.url_main = url_main
        self.url_home = url_home

    def getContext(self, form_tags, form_new_tag, select_technique):
        if select_technique == "general":
            self.url_main = "cata_system:seleccion_tecnica"
            self.url_home = "cata_system:index"

        return {
            "form_tags": form_tags,
            "form_new_tag": form_new_tag,
            "use_technique": self.technique_name,
            "url_main": reverse(self.url_main),
            "url_home": reverse(self.url_home),
        }

    def controllGet(self, request: HttpRequest, data):
        (
            type_scale,
            tamano_escala,
            form_new_etiqueta
        ) = self.defineInfoScale(data)

        form_etiqutas = SesionTagsForm(
            longitud=tamano_escala, tipo_escala=type_scale.nombre_escala)

        context_tags = self.getContext(
            form_tags=form_etiqutas,
            form_new_tag=form_new_etiqueta,
            select_technique=request.session.get("technique_selected")
        )

        return render(request, self.template, context_tags)

    def controllPost(self, request: HttpRequest, data):
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

        if form.is_valid():
            for name, value in form.cleaned_data.items():
                values[name] = value.id

            request.session["form_tags"] = values
            response = redirect(
                reverse("cata_system:panel_configuracion_codes"))

        else:
            context_tags = self.getContext(
                form_tags=form,
                form_new_tag=form_new_etiqueta,
                select_technique=request.session.get("technique_selected")
            )

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
