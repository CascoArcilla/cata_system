from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from ..forms import SesionTagsForm, EtiquetaForm
from ..models import TipoEscala

def configuracionPanelTags(req: HttpRequest):
    basic_data = req.session.get("form_basic", {})

    if not basic_data:
        return redirect(reverse('cata_system:panel_configuracion_basic'))
    
    tipo_escala = TipoEscala.objects.get(pk=basic_data["tipo_escala"])
    tamano_escala = basic_data["tamano_escala"]
    form_new_etiqueta = EtiquetaForm()

    if req.method == "GET":
        form_etiqutas = SesionTagsForm(longitud=tamano_escala, tipo_escala=tipo_escala.nombre_escala)

        context_tags = {
            "form_tags":form_etiqutas,
            "form_new_tag": form_new_etiqueta
        }

        return render(req, "tecnicas/configuracion-panel-tags.html", context_tags)
    elif req.method == "POST":
        values = {}
        form = SesionTagsForm(req.POST, longitud=tamano_escala, tipo_escala=tipo_escala.nombre_escala)

        context_tags = {
            "form_tags":form,
            "form_new_tag": form_new_etiqueta
        }

        if form.is_valid():
            for name, value in form.cleaned_data.items():
                values[name] = value.id

            req.session["form_tags"] = values
            return render(req, "tecnicas/configuracion-panel-tags.html", context_tags)
        else:
            context_tags["error"] = "ha ocurrido un error"
            return render(req, "tecnicas/configuracion-panel-tags.html", context_tags)