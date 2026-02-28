from django.http import HttpRequest
from django.shortcuts import render
from controllers import ConfTagsController
from utils.delete_data_session import deleteDataSession
from analist.decorators.required_analist import required_analist
from django.shortcuts import redirect
from django.urls import reverse


@required_analist(technique="escalas")
def conf_tags(request: HttpRequest):
    if not request.session.get("form_basic"):
        deleteDataSession(request)
        return redirect(reverse('analist:scales:conf_basic_scales') + "?error=datos requeridos no encontrados")

    basic_data = request.session.get("form_basic")
    template = "scales/conf-tags-sacales.html"

    if request.method == "GET":
        return ConfTagsController.get(request, basic_data, template_name=template)
    elif request.method == "POST":
        return ConfTagsController.post(request, basic_data, template_name=template, next_url='analist:scales:conf_codes_scales')
    else:
        return redirect(reverse('analist:scales:conf_basic_scales') + "?error=metodo no permitido")
