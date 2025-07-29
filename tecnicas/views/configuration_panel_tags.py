from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from ..forms import SesionTagsForm

def configuracionPanelTags(req: HttpRequest):
    # basic_data = req.session.get("basic_form", None)

    # if basic_data is None:
    #     return redirect(reverse('cata_system:panel_configuracion_basic'))

    etiquetas = SesionTagsForm(segmentos=5)
    return render(req, "tecnicas/configuracion-panel-tags.html", {"form_tags":etiquetas})