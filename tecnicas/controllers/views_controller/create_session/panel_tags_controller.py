from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from tecnicas.forms import SesionTagsForm, EtiquetaForm
from tecnicas.models import TipoEscala


class PanelTagsController():
    def __init__(self):
        pass

    @staticmethod
    def controllGetConvencional(request: HttpRequest, data):
        (
            type_scale,
            tamano_escala,
            form_new_etiqueta
        ) = PanelTagsController.defineInfoScale(data)

        form_etiqutas = SesionTagsForm(
            longitud=tamano_escala, tipo_escala=type_scale.nombre_escala)

        context_tags = {
            "form_tags": form_etiqutas,
            "form_new_tag": form_new_etiqueta
        }

        return render(request, "tecnicas/create_sesion/configuracion-panel-tags.html", context_tags)

    @staticmethod
    def controllPostConvencional(request: HttpRequest, data):
        (
            type_scale,
            tamano_escala,
            form_new_etiqueta
        ) = PanelTagsController.defineInfoScale(data)

        values = {}
        form = SesionTagsForm(request.POST, longitud=tamano_escala,
                              tipo_escala=type_scale.nombre_escala)

        context_tags = {
            "form_tags": form,
            "form_new_tag": form_new_etiqueta
        }

        if form.is_valid():
            for name, value in form.cleaned_data.items():
                values[name] = value.id

            request.session["form_tags"] = values
            response = redirect(
                reverse("cata_system:panel_configuracion_codes"))
        else:
            context_tags["error"] = "ha ocurrido un error"
            response = render(
                request, "tecnicas/create_sesion/configuracion-panel-tags.html", context_tags)

        return response

    @staticmethod
    def defineInfoScale(data):
        type_scale = TipoEscala.objects.get(pk=data["tipo_escala"])
        tamano_escala = data["tamano_escala"]
        form_new_etiqueta = EtiquetaForm()

        return (
            type_scale,
            tamano_escala,
            form_new_etiqueta
        )
